from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import Developer, Client, GenderList
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm


YES_NO_CHOICES = (
    (True, _('Yes')),
    (False, _('No')),
)


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
        self.fields['last_name'].required = True
        self.fields['mobile'].required = True
        self.fields['email'].required = True
        self.fields['gender'].required = True
        self.fields['gender'].widget = forms.RadioSelect(choices=GenderList.choices)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        return email


class ClientProfileForm(UserChangeForm):
    class Meta():
        model = Client
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'nationality',
            'city',
            'phone',
            'mobile',
            'address',
            'photo',
        ]

    widgets = {
        'birth_date': DateInput(),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['nationality'].required = True


class DeveloperCreationForm(ClientCreationForm):
    class Meta(ClientCreationForm.Meta):
        model = Developer
        fields = ClientCreationForm.Meta.fields + [
            'is_company',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_company'].widget = forms.RadioSelect(choices=YES_NO_CHOICES)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if 'gmail' in email or 'yahoo' in email or 'hotmail' in email:
            raise ValidationError(_('You have to enter an official email address'))
        email = email.lower()
        return email


class DeveloperProfileForm(ClientProfileForm):
    class Meta(ClientProfileForm.Meta):
        model = Developer
        fields = ClientProfileForm.Meta.fields + [
            'is_company',
            'company_name',
            'web_site',
            'trade_record',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        is_company = cleaned_data.get('is_company')
        company_name = cleaned_data.get('company_name')
        web_site = cleaned_data.get('web_site')
        trade_record = cleaned_data.get('trade_record')

        if is_company:
            if not company_name:
                raise forms.ValidationError(_('You have to enter a company name'))
            if not trade_record:
                raise forms.ValidationError(_('You have to enter a your company commercial license'))

        if not is_company and (company_name or trade_record or web_site):
            raise ValidationError(_('You are not a company'))

        return cleaned_data


class ForgetPasswordForm(PasswordResetForm):
    class Meta:
        model = Client
