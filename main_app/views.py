from django.shortcuts import render, HttpResponse
from django.views.generic import FormView, ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Project, Subscription, ProjectImage
from accounts.models import Client
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from accounts.views import ClientMixin, DeveloperMixin
from django.views.generic.edit import CreateView
from .forms import AddProjectForm, ProjectsSearchForm
from accounts.views import DeveloperMixin


class ProjectsListView(ListView):
    model = Project
    template_name = "main_app/projects_list.html"
    context_object_name = "projects"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_form'] = ProjectsSearchForm(self.request.GET or None)  # ProjectsSearchForm(self.request.GET or None)  #TODO: make a form for search and load it its initial with request.GET
        context['listing_title'] = _('All Projects')
        return context

    def get_queryset(self, *args, **kwargs):
        get_title = self.request.GET.get('title')
        get_type = self.request.GET.get('type')
        get_status = self.request.GET.get('status')

        query_set = Project.objects.all()

        if get_title:
            query_set = query_set.filter(name__icontains=get_title)

        if get_type:
            query_set = query_set.filter(type=get_type)

        if get_status:
            query_set = query_set.filter(statue=get_status)

        return query_set


class DeveloperProjectsListView(DeveloperMixin, ProjectsListView):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(developer=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['listing_title'] = _('My Projects')
        return context


class ClientSubscribedProjectsListView(ClientMixin, ProjectsListView):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            pk__in=Subscription.objects.filter(client=self.request.user).values_list('project', flat=True)
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['listing_title'] = _('My Subscribed Projects')
        return context


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
