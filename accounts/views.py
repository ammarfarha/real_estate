from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Developer


class ClientMixin(LoginRequiredMixin):
    pass


class DeveloperMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        user = self.request.user
        developer = Developer.objects.filter(username=user.username)
        return developer.exists()


class DeveloperTest(DeveloperMixin, TemplateView):
    template_name = 'blank.html'


def client_signup(request):
    return render(request, 'register.html')


def developer_signup(request):
    return render(request, 'signup.html')


def sign_in(request):
    return render(request, 'signup.html')


def sign_out(request):
    return render(request, 'signup.html')


def forget_password(request):
    return render(request, 'signup.html')
