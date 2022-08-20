from django.shortcuts import render, HttpResponse
from django.views.generic import FormView, ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Project, Subscription, ProjectImage
from accounts.models import Client
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from accounts.views import ClientMixin, DeveloperMixin
from django.views.generic.edit import CreateView
from .forms import AddProjectForm
from accounts.views import DeveloperMixin
from django.db.models import Q


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


class SearchResultsView(DisplayAllProject):
    def get_queryset(self, *args, **kwargs):
        get_title = self.request.GET.get('title')
        get_type = self.request.GET.get('type')
        get_status = self.request.GET.get('status')

        # query_set = Project.objects.all().order_by('developer')

        # if get_title is not None and get_title != "":
        #     q1 = Q(name__icontains=get_title)
        #     query_set.filter(name__icontains=get_title)
        # else:
        #     q1 = ()
            
        # if get_type is not None and get_type != "":
        #     query_set.filter(type=get_type)
        # if get_status is not None and get_status != "":
        #     query_set.filter(statue=get_status)

        query_set = Project.objects.filter(
            Q(name__icontains=get_title) if get_title else Q(),
            Q(type=get_type) if get_type else Q(),
            Q(statue=get_status) if get_status else Q(),
        ).order_by('developer')
        return query_set


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


class ProjectDetailsView(DetailView):
    model = Project
    template_name = 'main_app/project_detail.html'
    context_object_name = 'project'


class ProjectAddImageViews(CreateView):
    model = ProjectImage
    template_name = 'main_app/project_detail.html'
    form_class = 'addProjectImageFileForm'
    context_object_name = 'images'


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
