from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from .models import Project, Developer
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language, activate, gettext


def home(request):
    projects = Project.objects.all()
    context = {
        'sample_text': _("Hello"),
        'projects': projects,
    }
    return render(request, 'home.html', context)


# class StaffBaseView(LoginRequiredMixin, UserPassesTestMixin):
#
#     def test_func(self):
#         user = self.request.user
#         if user.is_staff:
#             return True
#         else:
#             return False
#
#
# class Staff1View(StaffBaseView, ListView):
#     model = Developer
#     template_name = "home.html"
#
#
# class Staff2View(StaffBaseView, FormView):
#     model = Developer
#     template_name = "home.html"
