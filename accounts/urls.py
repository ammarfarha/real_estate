from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(success_url_allowed_hosts='main_app:my-project-list'), name='logout'),
    path('forget-password/', views.ResetPasswordView.as_view(), name='forget_password'),
    path('register_client/', views.ClientRegistrationView.as_view(), name='register-client'),
    path('register_developer/', views.DeveloperRegistrationView.as_view(), name='register-developer'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]