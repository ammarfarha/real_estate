from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import Input
from .models import Developer, Client


class ClientCreationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = "__all__"


class DeveloperCreationForm(ClientCreationForm):
    class Meta:
        model = Developer
        fields = '__all__'
