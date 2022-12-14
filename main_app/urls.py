from django.urls import path

from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('projects/', views.ProjectsListView.as_view(), name='projects'),
    path('projects/<int:sub_phase_pk>/upload/', views.UpdateFileUploadView.as_view(), name='update-attachment'),
    path('contact/', views.ContactUsView.as_view(), name='contact'),
    path('project/<int:pk>/', views.ProjectDetailsView.as_view(), name='project-details'),
    path('project/<int:pk>/main/phase/', views.ProjectMainPhaseCreateView.as_view(), name='create-main-phase'),
    path('project/<int:pk>/main/phase/<int:main_phase_pk>/', views.ProjectMainPhaseUpdateView.as_view(), name='update-main-phase'),
    path('project/<int:pk>/sub/phase/', views.ProjectSubPhaseCreateView.as_view(), name='create-sub-phase'),
    path('project/<int:pk>/sub/phase/<int:sub_phase_pk>/', views.ProjectSubPhaseUpdateView.as_view(), name='update-sub-phase'),
    path('project/phases/<int:project_pk>/', views.ProjectPhasesListView.as_view(), name='project-phases'),
    path('project/phases/subphases/<int:main_phase_pk>/', views.ProjectPhasesListView.as_view(), name='main_phase'),
    path('project/phases/subphases/updates/<int:sub_phase_pk>/', views.ProjectPhasesListView.as_view(), name='sub-phase'),
    path('project/phases/subphases/updates/<int:sub_phase_pk>/add/', views.AddSubPhaseUpdateView.as_view(), name='add-update'),
    path('subscriptions/', views.ClientSubscribedProjectsListView.as_view(), name='my-subscribe-list'),
    path('subscribe/<int:pk>/', views.ClientSubscribeProjectView.as_view(), name='subscribe'),
    path('subscribe/<int:ppk>/<int:cpk>/', views.ClientReferralSubscribe.as_view(), name='ref-subscribe'),
    path('my_projects/', views.DeveloperProjectsListView.as_view(), name='my-project-list'),
    path('my_projects/add/', views.ProjectCreateView.as_view(), name='add-project'),
    path('my_projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('my_projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('my_projects/<int:pk>/upload/', views.ProjectImagesUploadView.as_view(), name='upload-image'),

]
