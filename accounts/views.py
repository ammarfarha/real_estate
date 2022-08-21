from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, FormView, CreateView, DetailView, ListView, UpdateView
from .models import Developer, Client
from django.urls import reverse_lazy
from .forms import DeveloperCreationForm, ClientCreationForm, ForgetPasswordForm, ClientProfileForm, \
    DeveloperProfileForm
from django.utils.translation import gettext_lazy as _


class ClientMixin(LoginRequiredMixin):
    pass


class DeveloperMixin(ClientMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_developer()


class ProfileView(ClientMixin, ListView):
    model = Client
    template_name = 'accounts/profile.html'
    context_object_name = 'current'

    def get_queryset(self):
        current = Client.objects.get(username=self.request.user.username)
        if current.is_developer():
            current = Developer.objects.get(username=self.request.user.username)
        return current


class ClientRegistrationView(CreateView):
    model = Client
    template_name = "accounts/client-register.html"
    form_class = ClientCreationForm
    success_url = reverse_lazy('main_app:index')


class DeveloperRegistrationView(SuccessMessageMixin, CreateView):
    model = Developer
    template_name = "accounts/developer-register.html"
    form_class = DeveloperCreationForm
    success_message = _("congratulations, You have been successfully registered, You will receive a message that your "
                        "account has been activated")
    success_url = reverse_lazy('main_app:index')

    def form_valid(self, form):
        form.instance.is_active = False
        return super().form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/developer-register.html'
    success_message = "fff"
    success_url = reverse_lazy('accounts:login')


class DeveloperProfileUpdateView(DeveloperMixin, UpdateView):
    form_class = DeveloperProfileForm
    template_name = 'accounts/developer-register.html'  # TODO: change and define success_url

    def get_object(self, queryset=None):
        return self.request.user.get_developer()
