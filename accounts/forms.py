from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Developer, Client
from django.utils.translation import gettext_lazy as _


class ClientCreationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = [
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
        ]
        labels = {
            'first_name': _('First Name'),
        }
        help_texts = {
            'username': _('please Enter more than 8 chars'),
        }
        error_messages = {
            'first_name': {
                'max_length': _("This first name is too long."),
                'required': _('This Field is Required'),
            },
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-user',
                'id': 'username',
                'placeholder': 'User Name',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control form-control-user',
                'id': 'password_1',
                'placeholder': 'Password',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control form-control-user',
                'id': 'password2',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control form-control-user',
                'id': 'first_name',
                'placeholder': 'First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control form-control-user',
                'id': 'last_name',
                'placeholder': 'Last Name',
            }),
        }


class DeveloperCreationForm(ClientCreationForm):
    class Meta:
        model = Developer
        fields = '__all__'
