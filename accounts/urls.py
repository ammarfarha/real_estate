from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='sign-out'),
    # path('forget-password/', views.ForgitPasswordView.as_view(), name='forget_password'),

    path('register_client/', views.ClientRegistrationView.as_view(), name='register-client'),
    path('register_developer/', views.DeveloperRegistrationView.as_view(), name='register-developer'),
]