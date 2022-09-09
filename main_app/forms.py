from django import forms
from django.utils.translation import gettext_lazy as _
from leaflet.forms.widgets import LeafletWidget
from martor.fields import MartorFormField
from accounts.forms import DateInput
from .models import Project, ProjectImage, Subscription, MainPhase, SubPhase, SubPhaseUpdate, UpdateAttachment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Field


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'summary',
            'type',
            'area',
            'location',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].widget = LeafletWidget(
            attrs={
                # 'display_raw': True,
                'map_width': '600px',
                'map_height': '400px',
                'geom_type': 'POINT',
            }
        )
        self.fields['location'].required = True


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = [
            'image',
            'alt',
        ]


class UpdateAttachmentForm(forms.ModelForm):
    class Meta:
        model = UpdateAttachment
        fields = [
            'update',
            'update_file',
        ]


class MainPhaseForm(forms.ModelForm):
    class Meta:
        model = MainPhase
        fields = ['title', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SubPhaseForm(forms.ModelForm):
    class Meta:
        model = SubPhase
        fields = '__all__'

        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'completion_date': DateInput(),
        }

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phase'].queryset = project.main_phases.all()


class SubscriptionForm(forms.ModelForm):
    full_name = forms.CharField(
        label=_("Full Name"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'disabled': 'disabled',
                'class': 'form-control bg-light',
            }
        )
    )
    card_code = forms.CharField(
        label=_("Card Code"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'disabled': 'disabled',
                'class': 'form-control bg-light',
            }
        )
    )
    account_number = forms.CharField(
        label=_("For Account Number"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'disabled': 'disabled',
                'class': 'form-control bg-light',
            }
        )
    )
    price = forms.CharField(
        label=_("Price Of Subscribe"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'disabled': 'disabled',
                'class': 'form-control bg-light',
            }
        )
    )

    class Meta:
        model = Subscription
        fields = []

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.initial['full_name'] = user.first_name + " " + user.last_name
        self.initial['account_number'] = str('0123456789')
        self.initial['price'] = str('3000')


class ProjectsSearchForm(forms.Form):
    type = forms.ChoiceField(
        label=_('Type'),
        choices=Project.TypeList.choices,
    )
    title = forms.CharField(
        label=_('Project Title')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('type', css_class="col-lg-3 my-2"),
            Div('title', css_class="col-lg-7 my-2"),
        )
        self.fields['type'].required = False
        self.fields['type'].label = ''
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].required = False
        self.fields['title'].label = ''
        self.fields['title'].widget.attrs.update({'placeholder': ''})


class SubPhaseUpdateForm(forms.ModelForm):
    attachments = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    description = MartorFormField()

    class Meta:
        model = SubPhaseUpdate
        fields = [
            'description',
            'attachments',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, }),
        }
