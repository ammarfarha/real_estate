from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, FormView, CreateView
from .models import Developer, Client
from django.urls import reverse_lazy
from .forms import DeveloperCreationForm, ClientCreationForm, ForgetPasswordForm


class ClientMixin(LoginRequiredMixin):
    pass


class DeveloperMixin(ClientMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_developer()


class ClientRegistrationView(CreateView):
    model = Client
    template_name = "accounts/client-register.html"
    form_class = ClientCreationForm
    success_url = reverse_lazy('main_app:index')


class DeveloperRegistrationView(SuccessMessageMixin, CreateView):
    model = Developer
    template_name = "accounts/developer-register.html"
    form_class = DeveloperCreationForm
    success_message = "Developer Created .. "
    success_url = reverse_lazy('main_app:index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs['is_active'] = False
        print(kwargs)
        return kwargs


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/developer-register.html'
    success_message = "fff"
    success_url = reverse_lazy('users-home')
