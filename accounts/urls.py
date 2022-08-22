from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='main_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(success_url_allowed_hosts='main_app:my-project-list'), name='logout'),
    path('forget_password/', views.ResetPasswordView.as_view(), name='forget-password'),
    path('register_client/', views.ClientRegistrationView.as_view(), name='register-client'),
    path('register_developer/', views.DeveloperRegistrationView.as_view(), name='register-developer'),
    path('dev_profile/', views.DeveloperProfileUpdateView.as_view(), name='developer-profile'),
    path('cli_profile/', views.ClientProfileUpdateView.as_view(), name='client-profile'),
]
