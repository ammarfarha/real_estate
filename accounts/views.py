from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, FormView, CreateView
from .models import Developer, Client
from django.urls import reverse_lazy
from .forms import DeveloperCreationForm, ClientCreationForm, ForgetPasswordForm


class ClientMixin(LoginRequiredMixin):
    def test_func(self):
        user = self.request.user
        developer = Developer.objects.filter(username=user.username)
        clients = Client.objects.filter(username=user.username)
        return not developer.exists() and clients.exists()


class DeveloperMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        developer = Developer.objects.filter(username=user.username)
        return developer.exists()


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


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/developer-register.html'
    success_message = "fff"
    success_url = reverse_lazy('users-home')
