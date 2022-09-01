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
from accounts.views import (
    ClientMixin,
    DeveloperMixin,
)
from django.views.generic.edit import CreateView
from .forms import (
    ProjectForm,
    ProjectsSearchForm,
    ProjectImageForm,
    SubscriptionForm,
    SubPhaseUpdateForm,
    MainPhaseForm,
)
from accounts.views import DeveloperMixin
from accounts.models import Developer
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin


class ProjectCanEditMixin(DeveloperMixin):
    project = None

    def test_func(self):
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return super().test_func() and self.project.developer == self.request.user.get_developer()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context


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


class ProjectCreateView(DeveloperMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'dashboards/add_project.html'
    success_message = _("Your Project Have been Added Successfully")
    success_url = reverse_lazy('main:my-project-list')
    created_project_pk = None

    def form_valid(self, form):
        form.instance.developer = self.request.user.get_developer()
        form.instance.status = Project.StatusList.PLANING
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['listing_title'] = _('Add Project')
        return context

    def get_success_url(self):
        return reverse_lazy('main_app:upload-image', args=[self.object.pk, ])


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


class ProjectUpdateView(SuccessMessageMixin, ProjectCanEditMixin, UpdateView):
    model = Project
    template_name = 'dashboards/project_edit.html'
    form_class = ProjectForm
    context_object_name = 'project'
    success_message = _("Your Project Have Been Updated Successfully")

    def get_success_url(self):
        return reverse_lazy('main:project-update', args=[self.project.pk])

    def form_valid(self, form):
        form.instance.developer = self.request.user.get_developer()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['page_title'] = _('Project {project} Basic Info').format(project=self.project)
        return context


class ProjectImagesUploadView(SuccessMessageMixin, ProjectCanEditMixin, CreateView):
    form_class = ProjectImageForm
    template_name = 'dashboards/project_images_upload.html'
    success_message = _("Your Image Has been Uploaded Successfully")

    def form_valid(self, form):
        form.instance.project = self.project
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['page_title'] = _('Project {project} Images').format(project=self.project)
        return context

    def get_success_url(self):
        return reverse_lazy('main:upload-image', args=[self.project.pk, ])


class ProjectMainPhaseBaseView(SuccessMessageMixin, ProjectCanEditMixin):
    form_class = MainPhaseForm
    template_name = 'dashboards/project_main_phase.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['page_title'] = _('Project {project} Main-Phases').format(project=self.project)
        return context

    def get_success_url(self):
        return reverse_lazy('main_app:create-main-phase', args=(self.project.pk, ))


class ProjectMainPhaseCreateView(ProjectMainPhaseBaseView, CreateView):
    success_message = _('Main phase was added successfully')

    def form_valid(self, form):
        form.instance.project = self.project
        return super().form_valid(form)


class ProjectMainPhaseUpdateView(ProjectMainPhaseBaseView, UpdateView):
    success_message = _('Main phase was updated successfully')

    def get_object(self, queryset=None):
        return get_object_or_404(MainPhase, pk=self.kwargs.get('main_phase_pk'), project=self.project)


class ProjectDeleteView(SuccessMessageMixin, ProjectCanEditMixin, DeleteView):
    models = Project
    template_name = 'dashboards/delete.html'
    success_message = _("Your Project Have Been Deleted Successfully")
    success_url = reverse_lazy('main_app:my-project-list')

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


class ClientReferralSubscribe(ClientMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        client_pk = int(kwargs.get('cpk'))
        try:
            self.request.session['ref_client'] = client_pk
        except:
            pass
        return reverse_lazy('main_app:subscribe', kwargs={'pk': kwargs.get('ppk')})


class ClientSubscribeProjectView(SuccessMessageMixin, ClientMixin, CreateView):
    models = Subscription
    form_class = SubscriptionForm
    template_name = 'main/subscribe.html'
    success_message = _("Your Subscription Added Successfully")

    def car_subscribe(self):
        project = get_object_or_404(Project, id=self.kwargs.get('pk'))
        user = self.request.user
        return not Subscription.objects.filter(project=project, client=user).exists()

    def form_valid(self, form):
        if self.car_subscribe():
            form.instance.project = get_object_or_404(Project, id=self.kwargs.get('pk'))
            form.instance.client = self.request.user
            if self.request.session.get('ref_client'):
                form.instance.referral_user = get_object_or_404(Client, pk=self.request.session.get('ref_client'))
            else:
                form.instance.referral_user = None
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['can_subscribe'] = self.car_subscribe()
        return context


class AddSubPhaseUpdateView(SuccessMessageMixin, DeveloperMixin, CreateView):
    models = SubPhaseUpdate
    form_class = SubPhaseUpdateForm
    template_name = 'main/phases.html'
    success_message = _("Add Update Successfully")

    def form_valid(self, form):
        form.instance.sub_phase = get_object_or_404(SubPhase, pk=self.kwargs.get('spk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main_app:sub-phase-updates',
                            args=[self.kwargs.get('pk'), self.kwargs.get('mpk'), self.kwargs.get('spk')])
