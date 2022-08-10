from django.urls import path
from . import views
urlpatterns = [
    path('client-signup/', views.client_signup, name='client_signup'),
    path('developer-signup/', views.developer_signup, name='developer_signup'),
    path('sign-in/', views.sign_in, name='signin'),
    path('sign-out/', views.sign_out, name='signout'),
    path('forget-password/', views.forget_password, name='forget_password'),
]