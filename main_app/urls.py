from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('',                                                    views.ProjectsListView.as_view(),   name='index'),
    path('contact/',                                            views.ContactUsView.as_view(), name='contact'),
    path('project/<int:pk>/',                                   views.ProjectDetailsView.as_view(), name='project-details'),
    path('subscribe/<int:pk>/',                                 views.ClientSubscribeProjectView.as_view(), name='subscribe'),
    path('subscribe/<int:ppk>/<int:cpk>/',                      views.ClientReferralSubscribe.as_view(), name='ref-subscribe'),
    path('my_projects/',                                        views.DeveloperProjectsListView.as_view(), name='my-project-list'),
    path('my_projects/add/',                                    views.ProjectAddView.as_view(), name='add-project'),
    path('my_projects/<int:pk>/update/',                        views.ProjectUpdateView.as_view(), name='project-update'),
    path('my_projects/<int:pk>/delete/',                        views.ProjectDeleteView.as_view(), name='project-delete'),
    path('my_projects/<int:pk>/upload/',                        views.ProjectUploadImageView.as_view(), name='upload-image'),

    # path('project/phases/<int:project_pk>/',                        views.ProjectPhasesListView.as_view(), name='project-phases'),
    # path('project/phases/subphases/<int:main_phase_pk>/',                        views.ProjectPhasesListView.as_view(), name='project-phases'),
    # path('project/phases/subphases/updates/<int:sub_phase_pk>/',                        views.ProjectPhasesListView.as_view(), name='project-phases'),
    path('my_projects/<int:pk>/phases/<int:mpk>/',              views.ProjectPhasesListView.as_view(), name='sub-phase'),
    path('my_projects/<int:pk>/phases/<int:mpk>/<int:spk>/',    views.ProjectPhasesListView.as_view(), name='sub-phase-updates'),
    path('my_projects/<int:pk>/phases/<int:mpk>/<int:spk>/add/',    views.AddSubPhaseUpdateView.as_view(), name='add-updates'),
]
