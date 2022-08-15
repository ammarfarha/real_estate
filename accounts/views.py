from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, CreateView
from .models import Developer, Client
from django.urls import reverse_lazy
from .forms import DeveloperCreationForm, ClientCreationForm


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
    template_name = "client-register.html"
    form_class = ClientCreationForm
    success_url = reverse_lazy('basic:index')


class DeveloperRegistrationView(CreateView):
    model = Developer
    template_name = "developer-register.html"
    form_class = DeveloperCreationForm
    success_url = reverse_lazy('basic:index')


# class DeveloperTest(DeveloperMixin, TemplateView):
#     template_name = 'blank.html'


# class ClientCreationView(CreateView):
#     model = Client
#     template_name = 'client-register.html'
#     form_class = ClientCreationForm
#     success_url = reverse_lazy('basic:index')
#
#
# class DeveloperCreationViews(FormView):
#     template_name = 'developer-register.html'
#     form_class = DeveloperCreationForm
#     success_url = reverse_lazy('index')
#
#
# def client_signup(request):
#     if request.method == 'POST':
#         form = ClientCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = ClientCreationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'register.html', context)
#
#
# def developer_signup(request):
#     if request.method == 'POST':
#         form = DeveloperCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = DeveloperCreationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'register.html', context)
#
#
# def sign_in(request):
#     return render(request, 'signup.html')
#
#
# def sign_out(request):
#     return render(request, 'signup.html')
#
#
# def forget_password(request):
#     return render(request, 'signup.html')
