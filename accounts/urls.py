from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='sign-out'),

    path('register_client/', views.ClientCreationView.as_view(), name='register-client'),
    path('register_developer/', views.ClientCreationView.as_view(), name='register-developer'),

    path('forget-password/', views.forget_password, name='forget_password'),
    path('test/', views.DeveloperTest.as_view(), name='test'),
]