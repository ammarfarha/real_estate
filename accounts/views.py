from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, FormView, CreateView, DetailView, ListView, UpdateView
from .models import Developer, Client
from django.urls import reverse_lazy
from .forms import DeveloperCreationForm, ClientCreationForm, ForgetPasswordForm, ClientProfileForm, \
    DeveloperProfileForm
from django.utils.translation import gettext_lazy as _
from main_app.forms import ProjectsSearchForm
from django.shortcuts import get_object_or_404


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
        current = get_object_or_404(Client, username=self.request.user.username)
        if current.is_developer():
            current = get_object_or_404(Developer, username=self.request.user.username)
        return current


class ClientRegistrationView(SuccessMessageMixin, CreateView):
    model = Client
    template_name = "main/registration.html"
    form_class = ClientCreationForm
    success_message = _("congratulations, You have been successfully registered")
    success_url = reverse_lazy('main:index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['listing_title'] = _('Create New Client')
        return context


class DeveloperRegistrationView(SuccessMessageMixin, CreateView):
    model = Developer
    template_name = "main/registration.html"
    form_class = DeveloperCreationForm
    success_message = _("congratulations, You have been successfully registered, You will receive a message that your "
                        "account has been activated")
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        form.instance.is_active = False
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['listing_title'] = _('Create New Developer')
        return context


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/user_form.html'
    success_message = _("Password Have been Rest Successfully")
    success_url = reverse_lazy('accounts:login')


class ClientProfileUpdateView(SuccessMessageMixin, UpdateView):
    model = Client
    template_name = 'dashboards/profile.html'
    form_class = ClientProfileForm
    success_message = _("Your Profile Updated Successfully.")
    success_url = reverse_lazy('accounts:client-profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # context['search_form'] = ProjectsSearchForm(self.request.GET or None)
        context['listing_title'] = _('Update Client Profile')
        context['bottom_title'] = _('Update')
        return context


class DeveloperProfileUpdateView(DeveloperMixin, ClientProfileUpdateView):
    model = Developer
    form_class = DeveloperProfileForm
    success_url = reverse_lazy('accounts:developer-profile')

    def get_object(self, queryset=None):
        return self.request.user.get_developer()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['listing_title'] = _('Update Developer Profile')
        return context
