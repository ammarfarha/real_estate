from django.shortcuts import render, HttpResponse
from django.views.generic import FormView, ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Project, Subscription
from accounts.models import Client
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from accounts.views import ClientMixin, DeveloperMixin
from django.views.generic.edit import CreateView
from .forms import AddProjectForm
from accounts.views import DeveloperMixin
def home(request):
    projects = Project.objects.all()
    clients = Client.objects.all()
    context = {
        'sample_text': _("Hello"),
        'projects': projects,
        'users': clients,
    }
    return render(request, 'main_app/project_list.html', context)


class DisplayAllProject(ListView):
    model = Project
    template_name = "main_app/developer_project_list.html"
    context_object_name = "projects"
    paginate_by = 5


class DeveloperListProject(DeveloperMixin, DisplayAllProject):
    def get_queryset(self, *args, **kwargs):
        return Project.objects.filter(developer=self.request.user)


class ClientSubscribeProjects(ClientMixin, DisplayAllProject):
    def get_queryset(self, *args, **kwargs):
        return Project.objects.filter(
            pk__in=Subscription.objects.filter(client=self.request.user).values_list('project', flat=True)
        )


class ProjectAddView(DeveloperMixin, CreateView):
    model = Project
    form_class = AddProjectForm
    template_name = 'main_app/add_project.html'
    success_url = reverse_lazy('main_app:my-project-list')


class ProjectDetails(DetailView):
    model = Project
    template_name = 'main_app/project_detail.html'
    context_object_name = 'project'



class ProjectUpdate(UpdateView):
    model = Project
    template_name = 'main_app/project_detail.html'
    context_object_name = 'project'


class ProjectDelete(DeleteView):
    model = Project


class ProjectPhasesList(ListView):
    model = Project


class ProjectAdd:
    pass


class ProjectAdd:
    pass
