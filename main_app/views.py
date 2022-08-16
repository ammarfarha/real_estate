from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from .models import Project, Subscription
from accounts.models import Client
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language, activate, gettext
from accounts.views import ClientMixin, DeveloperMixin


def home(request):
    projects = Project.objects.all()
    clients = Client.objects.all()
    context = {
        'sample_text': _("Hello"),
        'projects': projects,
        'users': clients,
    }
    return render(request, 'project_list.html', context)
    # return render(request, 'buttons.html', context)


class DeveloperListProject(DeveloperMixin, ListView):
    model = Project
    template_name = "developer_project_list.html"
    context_object_name = "projects"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        return Project.objects.filter(developer=self.request.user)


class ClientSubscribeProjects(ClientMixin, ListView):
    model = Project
    template_name = "clients_project_list.html"
    context_object_name = "projects"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        proj = []
        subscription = Subscription.objects.filter(client=self.request.user)
        for sub in subscription:
            proj.append(sub.project)
        return proj

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


# class Staff2View(StaffBaseView, FormView):
#     model = Developer
#     template_name = "home.html"
