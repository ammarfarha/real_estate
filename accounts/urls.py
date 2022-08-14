from django.contrib.auth.views import LoginView
from django.urls import path
from . import views
urlpatterns = [
    path('client-signup/', views.client_signup, name='client_signup'),
    path('developer-signup/', views.developer_signup, name='developer_signup'),
    path('login/', LoginView.as_view(template_name='home.html'), name='login'),
    path('sign-out/', views.sign_out, name='signout'),
    path('forget-password/', views.forget_password, name='forget_password'),
    path('test/', views.DeveloperTest.as_view(), name='test'),
]