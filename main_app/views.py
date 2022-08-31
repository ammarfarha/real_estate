from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.generic import (
    FormView,
    ListView,
    CreateView,
    DetailView,
    DeleteView,
    UpdateView,
    TemplateView,
    RedirectView,
)
from .models import (
    Project,
    Subscription,
    ProjectImage,
    MainPhase,
    SubPhase,
    SubPhaseUpdate,
)
from accounts.models import Client
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from accounts.views import ClientMixin, DeveloperMixin
from django.views.generic.edit import CreateView
from .forms import AddProjectForm, ProjectsSearchForm, AddProjectImageFileForm, SubscriptionForm, SubPhaseUpdateForm
from accounts.views import DeveloperMixin
from accounts.models import Developer
from django.shortcuts import get_object_or_404


class ProjectCanEditMixin(DeveloperMixin):
    def test_func(self):
        return super().test_func() and self.get_object().developer == self.request.user.get_developer()


class ProjectsListView(ListView):
    model = Project
    template_name = "main/projects.html"
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


class ContactUsView(TemplateView):
    template_name = "main/contact.html"


class DeveloperProjectsListView(DeveloperMixin, ProjectsListView):
    template_name = "dashboards/my_admin.html"

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
    success_url = reverse_lazy('main:my-project-list')

    def form_valid(self, form):
        form.instance.developer = get_object_or_404(Developer, username=self.request.user.username)
        form.instance.status = 'PL'
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_form'] = ProjectsSearchForm(self.request.GET or None)
        context['listing_title'] = _('Add Project')
        return context


class ProjectDetailsView(ClientMixin, DetailView):
    model = Project
    template_name = 'main/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['listing_title'] = _('Display Project')
        context['project_images'] = self.object.project_images.all()
        context['can_edit'] = self.object.can_edit(self.request.user)
        context['can_subscribe'] = self.object.can_subscribe(self.request.user)
        context['is_subscribed'] = self.object.is_subscribed(self.request.user)
        context['main_phases'] = self.object.main_phases.all()
        context['free_phase'] = self.object.main_phases.all().first()
        return context


class ProjectAddImageViews(ProjectCanEditMixin, CreateView):
    model = ProjectImage
    template_name = 'main/project_detail.html'

    def test_func(self):
        return super().test_func()


class AddProjectMainPhasesView(ProjectCanEditMixin, CreateView):
    model = ProjectImage
    template_name = 'main/project_detail.html'


class AddProjectSubPhaseView(ProjectCanEditMixin, CreateView):
    model = ProjectImage
    template_name = 'main/project_detail.html'


class AddProjectSubPhaseUpdateView(ProjectCanEditMixin, CreateView):
    model = ProjectImage
    template_name = 'main/project_detail.html'


class ProjectUpdateView(ProjectCanEditMixin, UpdateView):
    model = Project
    template_name = 'dashboards/project_edit.html'
    form_class = AddProjectForm
    context_object_name = 'project'

    def get_success_url(self):
        return reverse_lazy('main:project-update', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.developer = get_object_or_404(Developer, username=self.request.user.username)
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


class ProjectPhasesListView(DeveloperMixin, ListView):
    model = SubPhaseUpdate
    template_name = "main/phases.html"
    context_object_name = "updates"
    paginate_by = 3

    def get_project(self, *args, **kwargs):
        return get_object_or_404(Project, pk=self.kwargs.get('pk'))

    def get_main_phase(self, *args, **kwargs):
        if self.kwargs.get('mpk'):
            return get_object_or_404(MainPhase, pk=self.kwargs.get('mpk'))
        else:
            return MainPhase.objects.filter(project=self.get_project()).first()

    def get_sub_phase(self, *args, **kwargs):
        if self.kwargs.get('spk'):
            return get_object_or_404(SubPhase, pk=self.kwargs.get('spk'))
        else:
            return SubPhase.objects.filter(phase=self.get_main_phase()).first()

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(sub_phase=self.get_sub_phase())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['project'] = self.get_project()
        context['main_phase'] = self.get_main_phase()
        context['sub_phase'] = self.get_sub_phase()
        context['addForm'] = SubPhaseUpdateForm
        return context


class ProjectUploadImageView(DeveloperMixin, CreateView):
    models = ProjectImage
    form_class = AddProjectImageFileForm
    template_name = 'dashboards/profile.html'

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, id=self.request.POST['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main:project-update', args=[self.request.POST['pk']])


class ClientReferralSubscribe(ClientMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        client_pk = int(kwargs.get('cpk'))
        try:
            self.request.session['ref_client'] = client_pk
        except:
            pass
        return reverse_lazy('main_app:subscribe', kwargs={'pk': kwargs.get('ppk')})


class ClientSubscribeProjectView(ClientMixin, CreateView):
    models = Subscription
    form_class = SubscriptionForm
    template_name = 'main/subscribe.html'

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, id=self.kwargs.get('pk'))
        form.instance.client = self.request.user
        try:
            if self.request.session.get('ref_client'):
                form.instance.referral_user = get_object_or_404(Client, pk=self.request.session.get('ref_client'))
            else:
                form.instance.referral_user = None
        except:
            pass
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main:index')


class AddSubPhaseUpdateView(DeveloperMixin, CreateView):
    models = SubPhaseUpdate
    form_class = SubPhaseUpdateForm
    template_name = 'main/phases.html'

    def form_valid(self, form):
        form.instance.sub_phase = get_object_or_404(SubPhase, pk=self.kwargs.get('spk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main_app:sub-phase-updates', args=[self.kwargs.get('pk'), self.kwargs.get('mpk'), self.kwargs.get('spk')])
