from django.urls import path

from django_ledger import views

urlpatterns = [
    path('<slug:entity_slug>/lastest/',
         views.InvoiceModelListView.as_view(),
         name='invoice-list'),
    path('<slug:entity_slug>/year/<int:year>/',
         views.InvoiceModelYearlyListView.as_view(),
         name='invoice-list-year'),
    path('<slug:entity_slug>/month/<int:year>/<int:month>/',
         views.InvoiceModelMonthlyListView.as_view(),
         name='invoice-list-month'),
    path('<slug:entity_slug>/create/',
         views.InvoiceModelCreateView.as_view(),
         name='invoice-create'),
    path('<slug:entity_slug>/create/estimate/<uuid:ce_pk>/',
         views.InvoiceModelCreateView.as_view(for_estimate=True),
         name='invoice-create-estimate'),
    path('<slug:entity_slug>/detail/<uuid:invoice_pk>/',
         views.InvoiceModelDetailView.as_view(),
         name='invoice-detail'),
    path('<slug:entity_slug>/update/<uuid:invoice_pk>/',
         views.InvoiceModelUpdateView.as_view(),
         name='invoice-update'),
    path('<slug:entity_slug>/update/<uuid:invoice_pk>/items/',
         views.InvoiceModelUpdateView.as_view(action_update_items=True),
         name='invoice-update-items'),
    path('<slug:entity_slug>/delete/<uuid:invoice_pk>/',
         views.InvoiceModelDeleteView.as_view(),
         name='invoice-delete'),

    # actions...
    path('<slug:entity_slug>/actions/<uuid:invoice_pk>/mark-as-draft/',
         views.InvoiceModelActionMarkAsDraftView.as_view(),
         name='invoice-action-mark-as-draft'),
    path('<slug:entity_slug>/actions/<uuid:invoice_pk>/mark-as-review/',
         views.InvoiceModelActionMarkAsReviewView.as_view(),
         name='invoice-action-mark-as-review'),
    path('<slug:entity_slug>/actions/<uuid:invoice_pk>/mark-as-approved/',
         views.InvoiceModelActionMarkAsApprovedView.as_view(),
         name='invoice-action-mark-as-approved'),
    path('<slug:entity_slug>/actions/<uuid:invoice_pk>/mark-as-paid/',
         views.InvoiceModelActionMarkAsPaidView.as_view(),
         name='invoice-action-mark-as-paid'),
    path('<slug:entity_slug>/actions/<uuid:invoice_pk>/mark-as-canceled/',
         views.InvoiceModelActionMarkAsCanceledView.as_view(),
         name='invoice-action-mark-as-canceled'),
    path('<slug:entity_slug>/actions/<uuid:invoice_pk>/mark-as-void/',
         views.InvoiceModelActionMarkAsVoidView.as_view(),
         name='invoice-action-mark-as-void'),

    path('<slug:entity_slug>/actions/<uuid:invoice_pk>/force-migrate/',
         views.InvoiceModelActionForceMigrateView.as_view(),
         name='invoice-action-force-migrate'),
    path('<slug:entity_slug>/actions/<uuid:invoice_pk>/lock/',
         views.InvoiceModelActionLockLedgerView.as_view(),
         name='invoice-action-lock-ledger'),
    path('<slug:entity_slug>/actions/<uuid:invoice_pk>/unlock/',
         views.InvoiceModelActionUnlockLedgerView.as_view(),
         name='invoice-action-unlock-ledger'),

]
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)