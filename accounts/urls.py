from allauth.account.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/reset/', views.ResetPasswordView.as_view(), name='forget-password'),
    path('password/change/', PasswordChangeView.as_view(), name='change-password'),
    path('register_client/', views.ClientRegistrationView.as_view(), name='register-client'),
    path('register_developer/', views.DeveloperRegistrationView.as_view(), name='register-developer'),
    path('dev_profile/', views.DeveloperProfileUpdateView.as_view(), name='developer-profile'),
    path('cli_profile/', views.ClientProfileUpdateView.as_view(), name='client-profile'),
]
