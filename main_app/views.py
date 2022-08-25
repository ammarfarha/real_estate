from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.generic import FormView, ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Project, Subscription, ProjectImage
from accounts.models import Client
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from accounts.views import ClientMixin, DeveloperMixin
from django.views.generic.edit import CreateView
from .forms import AddProjectForm, ProjectsSearchForm, AddProjectImageFileForm, SubscriptionForm
from accounts.views import DeveloperMixin
from accounts.models import Developer


class ProjectCanEditMixin(DeveloperMixin):
    def test_func(self):
        return super().test_func() and self.get_object().developer == self.request.user.get_developer()


class ProjectsListView(ListView):
    model = Project
    template_name = "main_app/projects_list.html"
    context_object_name = "projects"
    paginate_by = 9

    # TODO: make a form for search and load it its initial with request.GET
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_form'] = ProjectsSearchForm(
            self.request.GET or None)
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


class AdminProjectsListView(DeveloperMixin, ProjectsListView):
    template_name = "dashboards/my_admin.html"


class DeveloperProjectsListView(DeveloperMixin, ProjectsListView):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(developer=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['listing_title'] = _('My Projects')
        return context


class AdminDeveloperProjectsListView(AdminProjectsListView):
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
    template_name = 'dashboards/add_project.html'
    success_url = reverse_lazy('main_app:admin-my-project-list')

    def form_valid(self, form):
        form.instance.developer = Developer.objects.get(username=self.request.user.username)
        form.instance.status = 'PL'
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_form'] = ProjectsSearchForm(self.request.GET or None)
        context['listing_title'] = _('Add Project')
        return context


class ProjectDetailsView(ProjectCanEditMixin, DetailView):
    model = Project
    template_name = 'main_app/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['listing_title'] = _('Dispaly Project')
        context['project_images'] = self.object.project_images.all()
        return context


class ProjectAddImageViews(ProjectCanEditMixin, CreateView):
    model = ProjectImage
    template_name = 'main_app/project_detail.html'

    def test_func(self):
        return super().test_func()


class AddProjectMainPhasesView(ProjectCanEditMixin, CreateView):
    model = ProjectImage
    template_name = 'main_app/project_detail.html'


class AddProjectSubPhaseView(ProjectCanEditMixin, CreateView):
    model = ProjectImage
    template_name = 'main_app/project_detail.html'


class AddProjectSubPhaseUpdateView(ProjectCanEditMixin, CreateView):
    model = ProjectImage
    template_name = 'main_app/project_detail.html'


class ProjectUpdateView(ProjectCanEditMixin, UpdateView):
    model = Project
    template_name = 'dashboards/project_edit.html'
    form_class = AddProjectForm
    context_object_name = 'project'

    def get_success_url(self):
        return reverse_lazy('main_app:project-update', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.developer = Developer.objects.get(username=self.request.user.username)
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['upload_imag_form'] = AddProjectImageFileForm()
        context['listing_title'] = _('Add Project')
        context['project_images'] = ProjectImage.objects.filter(project_id=self.object.pk)
        return context


class ProjectDeleteView(ProjectCanEditMixin, DeleteView):
    models = Project
    template_name = 'dashboards/delete.html'
    success_url = reverse_lazy('main_app:admin-my-project-list')

    def test_func(self):
        return super().test_func() and self.get_object().developer == self.request.user.get_developer()

    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(Project, id=id_)


class ProjectPhasesListView(ClientMixin, ListView):
    model = Project


class ProjectUploadImageView(DeveloperMixin, CreateView):
    models = ProjectImage
    form_class = AddProjectImageFileForm
    template_name = 'dashboards/profile.html'

    def form_valid(self, form):
        form.instance.project = Project.objects.get(id=self.request.POST['pk'])
        # form.instance.image = self.request.FILES['image']
        # form.instance.alt = self.request.POST['alt']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main_app:project-update', args=[self.request.POST['pk']])


class ClientSubscribeProjectView(ClientMixin, CreateView):
    models = Subscription
    form_class = SubscriptionForm
    template_name = 'main_app/subscribe.html'

    def form_valid(self, form):
        form.instance.project = Project.objects.get(id=self.kwargs.get('pk'))
        form.instance.client = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main_app:index')


