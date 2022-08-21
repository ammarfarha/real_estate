from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import Developer, Client
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm


class DateInput(forms.DateInput):
    input_type = 'date'


class ClientCreationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = [
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'mobile',
            'email',
            'gender',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].required = True


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'phone',
            'mobile',
            'email',
            'nationality',
            'gender',
            'city',
            'address',
            'photo',
        ]
        widgets = {
            'birth_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class DeveloperCreationForm(ClientCreationForm):
    class Meta(ClientCreationForm.Meta):
        model = Developer
        fields = ClientCreationForm.Meta.fields + [
            'is_company',
        ]


class DeveloperProfileForm(ClientProfileForm):
    class Meta(ClientProfileForm.Meta):
        model = Developer
        fields = ClientProfileForm.Meta.fields + [
            'is_company',
            'company_name',
            'web_site',
            'trade_record',
        ]


class ForgetPasswordForm(PasswordResetForm):
    class Meta:
        model = Client
