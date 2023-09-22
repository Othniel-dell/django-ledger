"""
Django Ledger created by Miguel Sanda <msanda@arrobalytics.com>.
Copyright© EDMA Group Inc licensed under the GPLv3 Agreement.

Contributions to this module:
Miguel Sanda <msanda@arrobalytics.com>
"""

from itertools import chain

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, FormView, DetailView

from django_ledger.forms.data_import import OFXFileImportForm
from django_ledger.forms.data_import import StagedTransactionModelFormSet
from django_ledger.io.ofx import OFXFileManager
from django_ledger.models.accounts import AccountModel
from django_ledger.models.data_import import ImportJobModel, StagedTransactionModel
from django_ledger.views.mixins import DjangoLedgerSecurityMixIn


class ImportJobModelViewQuerySetMixIn:
    queryset = None

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = ImportJobModel.objects.for_entity(
                entity_slug=self.kwargs['entity_slug'],
                user_model=self.request.user
            ).select_related('bank_account_model',
                             'bank_account_model__entity_model',
                             'bank_account_model__cash_account',
                             'bank_account_model__cash_account__coa_model')
        return super().get_queryset()


def digest_staged_txs(cleaned_staged_tx: dict, cash_account: AccountModel):
    tx_amt = cleaned_staged_tx['amount']
    reverse_tx = tx_amt < 0
    return [
        {
            'account_id': cash_account.uuid,
            'amount': abs(tx_amt),
            'tx_type': 'debit' if not reverse_tx else 'credit',
            'description': cleaned_staged_tx['name'],
            'staged_tx_model': cleaned_staged_tx['uuid']
        },
        {
            'account_id': cleaned_staged_tx['earnings_account'].uuid,
            'amount': abs(tx_amt),
            'tx_type': 'credit' if not reverse_tx else 'debit',
            'description': cleaned_staged_tx['name'],
            'staged_tx_model': cleaned_staged_tx['uuid']
        }
    ]


class DataImportJobsListView(DjangoLedgerSecurityMixIn, ImportJobModelViewQuerySetMixIn, ListView):
    PAGE_TITLE = _('Data Import Jobs')
    extra_context = {
        'page_title': PAGE_TITLE,
        'header_title': PAGE_TITLE
    }
    context_object_name = 'import_jobs'
    template_name = 'django_ledger/data_import/data_import_job_list.html'


class DataImportOFXFileView(DjangoLedgerSecurityMixIn, FormView):
    template_name = 'django_ledger/data_import/data_import_ofx.html'
    PAGE_TITLE = _('OFX File Import')
    extra_context = {
        'page_title': PAGE_TITLE,
        'header_title': PAGE_TITLE
    }
    form_class = OFXFileImportForm

    def get_success_url(self):
        return reverse('django_ledger:data-import-jobs-list',
                       kwargs={
                           'entity_slug': self.kwargs['entity_slug']
                       })

    def form_valid(self, form):
        ofx = OFXFileManager(ofx_file_or_path=form.files['ofx_file'])

        # Pulls accounts from OFX file...
        account_models = ofx.get_accounts()
        ofx_account_number = [a['account_number'] for a in account_models]

        # OFX file has multiple statements in it... Not supported...
        # All transactions must come from a single account...
        if len(ofx_account_number) > 1:
            messages.add_message(
                self.request,
                level=messages.ERROR,
                message=_('Multiple statements detected. Multiple account import is not supported.'),
                extra_tags='is-danger'
            )
            return self.form_invalid(form=form)

        ofx_account_number = ofx_account_number[0]

        # account has not been created yet...
        try:
            ba_model = self.AUTHORIZED_ENTITY_MODEL.bankaccountmodel_set.filter(
                account_number__exact=ofx_account_number
            ).select_related('cash_account', 'entity_model').get()
        except ObjectDoesNotExist:
            create_url = reverse(
                viewname='django_ledger:bank-account-create',
                kwargs={
                    'entity_slug': self.AUTHORIZED_ENTITY_MODEL.slug
                }
            )
            create_link = format_html('<a href={}>create</a>', create_url)
            messages.add_message(
                self.request,
                level=messages.ERROR,
                message=_(f'Account Number ***{ofx_account_number[-4:]} not recognized. Please {create_link} Bank '
                          'Account model before importing transactions'),
                extra_tags='is-danger'
            )
            return self.form_invalid(form=form)

        # account is not active...
        if not ba_model.is_active():
            create_url = reverse(
                viewname='django_ledger:bank-account-update',
                kwargs={
                    'entity_slug': self.AUTHORIZED_ENTITY_MODEL.slug,
                    'bank_account_pk': ba_model.uuid
                }
            )
            activate_link = format_html('<a href={}>mark account active</a>', create_url)
            messages.add_message(
                self.request,
                level=messages.ERROR,
                message=_(f'Account Number ***{ofx_account_number[-4:]} not active. Please {activate_link} '
                          ' before importing new transactions'),
                extra_tags='is-danger'
            )
            return self.form_invalid(form=form)

        import_job = ba_model.importjobmodel_set.create(
            description='OFX Import for Account ***' + ba_model.account_number[-4:]
        )
        txs_to_stage = ofx.get_account_txs(account=ba_model.account_number)
        staged_txs_model_list = [
            StagedTransactionModel(
                date_posted=tx.dtposted,
                fit_id=tx.fitid,
                amount=tx.trnamt,
                import_job=import_job,
                name=tx.name,
                memo=tx.memo
            ) for tx in txs_to_stage
        ]
        for tx in staged_txs_model_list:
            tx.clean()
        StagedTransactionModel.objects.bulk_create(staged_txs_model_list)
        return super().form_valid(form=form)


class DataImportJobDetailView(DjangoLedgerSecurityMixIn, ImportJobModelViewQuerySetMixIn, DetailView):
    template_name = 'django_ledger/data_import/data_import_job_txs.html'
    PAGE_TITLE = _('Import Job Staged Txs')
    context_object_name = 'import_job'
    pk_url_kwarg = 'job_pk'
    extra_context = {
        'page_title': PAGE_TITLE,
        'header_title': PAGE_TITLE
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_model: ImportJobModel = self.object
        context['header_title'] = job_model.bank_account_model
        bank_account_model = job_model.bank_account_model
        cash_account_model = job_model.bank_account_model.cash_account
        if not cash_account_model:
            bank_acct_url = reverse('django_ledger:bank-account-update',
                                    kwargs={
                                        'entity_slug': self.kwargs['entity_slug'],
                                        'bank_account_pk': bank_account_model.uuid
                                    })
            messages.add_message(
                self.request,
                messages.ERROR,
                mark_safe(f'Warning! No cash account has been set for {job_model.ledger.bankaccountmodel}. '
                          f'Importing has been disabled until Cash Account is assigned. '
                          f'Click <a href="{bank_acct_url}">here</a> to assign'),
                extra_tags='is-danger'
            )

        staged_txs_qs = job_model.stagedtransactionmodel_set.all()
        staged_txs_qs = staged_txs_qs.select_related('txs_model__account').order_by('-date_posted', '-amount')
        context['staged_txs_qs'] = staged_txs_qs

        txs_formset = StagedTransactionModelFormSet(
            user_model=self.request.user,
            entity_slug=self.kwargs['entity_slug'],
            exclude_account=cash_account_model,
            queryset=staged_txs_qs.is_imported(),
        )

        context['staged_txs_formset'] = txs_formset
        context['cash_account_model'] = cash_account_model
        context['bank_account_model'] = bank_account_model
        return context

    def post(self, request, **kwargs):
        job_model = self.get_object()
        self.object = job_model
        txs_formset = StagedTransactionModelFormSet(request.POST,
                                                    user_model=self.request.user,
                                                    entity_slug=kwargs['entity_slug'])
        if txs_formset.is_valid():
            txs_formset.save()
            staged_to_import = [
                tx for tx in txs_formset.cleaned_data if all([
                    tx['earnings_account'],
                    tx['tx_import'],
                    not tx['tx']
                ])
            ]

            if len(staged_to_import) > 0:
                job_model = ImportJobModel.objects.for_entity(
                    entity_slug=self.kwargs['entity_slug'],
                    user_model=self.request.user
                ).select_related(
                    'ledger__bankaccountmodel__cash_account'
                ).get(uuid__exact=self.kwargs['job_pk'])

                ledger_model = job_model.ledger
                cash_account = job_model.ledger.bankaccountmodel.cash_account

                txs_digest = list(chain.from_iterable(
                    digest_staged_txs(cleaned_staged_tx=tx,
                                      cash_account=cash_account) for tx in staged_to_import
                ))

                je_model, txs_models = ledger_model.commit_txs(
                    je_posted=True,
                    je_timestamp=now(),
                    je_txs=txs_digest,
                    je_desc='OFX Import JE',
                    je_activity='op'
                )

                staged_tx_models = [stx['uuid'] for stx in staged_to_import]
                StagedTransactionModel.objects.bulk_update(staged_tx_models, fields=['txs_model'])

            # txs_formset.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Successfully saved transactions.',
                                 extra_tags='is-success')
            return self.get(request, **kwargs)
        else:
            context = self.get_context_data(**kwargs)
            context['staged_txs_formset'] = txs_formset
            messages.add_message(request,
                                 messages.ERROR,
                                 'Hmmm, this doesn\'t add up!. Check your math!',
                                 extra_tags='is-danger')
            return self.render_to_response(context)
