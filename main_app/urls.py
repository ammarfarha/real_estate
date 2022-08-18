from django.urls import path, include
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.home, name='index'),
    path('my_projects/', views.DeveloperListProject.as_view(), name='my-project-list'),
    path('sub-projects/', views.ClientSubscribeProjects.as_view(), name='my-subscribed-list'),
]
