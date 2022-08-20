from django.urls import path, include
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.home, name='index'),
    path('my_projects/', views.DeveloperListProject.as_view(), name='my-project-list'),
    path('my_projects/add/', views.ProjectAddView.as_view(), name='add-project'),
    path('my_projects/<int:pk>/', views.ProjectDetails.as_view(), name='project-details'),
    path('my_projects/<int:id>/update/', views.ProjectUpdate.as_view(), name='project-update'),
    path('my_projects/<int:id>/delete/', views.ProjectDelete.as_view(), name='project-delete'),
    path('my_projects/<int:id>/phases/', views.ProjectPhasesList.as_view(), name='project-phases'),
    path('sub-projects/', views.ClientSubscribeProjects.as_view(), name='my-subscribed-list'),
]
