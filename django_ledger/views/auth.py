"""
Django Ledger created by Miguel Sanda <msanda@arrobalytics.com>.
Copyright© EDMA Group Inc licensed under the GPLv3 Agreement.

Contributions to this module:
    * Miguel Sanda <msanda@arrobalytics.com>
"""

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from django_ledger.forms.auth import LogInForm


class DjangoLedgerLoginView(LoginView):
    form_class = LogInForm
    template_name = 'django_ledger/auth/login.html'
    extra_context = {
        'page_title': _('Login')
    }

    def get_success_url(self):
        return reverse('django_ledger:home')


class DjangoLedgerLogoutView(LogoutView):
    next_page = reverse_lazy('django_ledger:login')


class DjangoLedgerSignuptView(LogoutView):
    template_name = 'django_ledger/auth/signup.html'
    next_page = reverse_lazy('django_ledger:login')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')

        if not all([username, email, firstname, lastname, password]):
            messages.error(request, 'All fields are required.')
            return render(request, self.template_name)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, self.template_name)

        user = User.objects.create_user(
            username=username, 
            password=password, 
            email=email, 
            first_name=firstname, 
            last_name=lastname
        )
        user.save()
        messages.success(request, 'Account created successfully.')
        return redirect(self.next_page)

