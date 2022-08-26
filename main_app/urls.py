from django.urls import path, include
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.ProjectsListView.as_view(), name='index'),
    path('my_projects/', views.DeveloperProjectsListView.as_view(), name='my-project-list'),
    path('my_projects/add/', views.ProjectAddView.as_view(), name='add-project'),
    path('my_projects/<int:pk>/', views.ProjectDetailsView.as_view(), name='project-details'),
    path('my_projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('my_projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('my_projects/<int:pk>/phases/', views.ProjectPhasesListView.as_view(), name='project-phases'),
    path('sub-projects/', views.ClientSubscribedProjectsListView.as_view(), name='my-subscribed-list'),
    path('my_projects/<int:pk>/upload/', views.ProjectUploadImageView.as_view(), name='upload-image'),
    path('subscribe/<int:pk>/', views.ClientSubscribeProjectView.as_view(), name='subscribe'),
]
