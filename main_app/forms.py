from django import forms
from leaflet.forms.fields import PointField
from accounts.forms import DateInput
from .models import Project, ProjectImage, Subscription, MainPhase, SubPhase, SubPhaseUpdate, UpdateAttachment
from django.utils.translation import gettext_lazy as _
from leaflet.forms.widgets import LeafletWidget
from django_countries.widgets import CountrySelectWidget


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
    FullName = forms.CharField(
        label=_("Full Name"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'value': "",
                'disabled': 'disabled',
            }
        )
    )
    email = forms.EmailField(
        label=_("Email Address"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'value': "",
                'disabled': 'disabled',
            }
        )
    )
    region = forms.CharField(
        label=_("Region"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'value': "",
                'disabled': 'disabled',
            }
        )
    )
    city = forms.CharField(
        label=_("City"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'value': "",
                'disabled': 'disabled',
            }
        )
    )
    address = forms.CharField(
        label=_("Address"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'value': "",
                'disabled': 'disabled',
            }
        )
    )
    card_code = forms.CharField(
        label=_("Card Code"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'value': "",
                'disabled': 'disabled',
            }
        )
    )
    account_number = forms.CharField(
        label=_("For Account Number"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'value': "",
                'disabled': 'disabled',
            }
        )
    )
    price = forms.CharField(
        label=_("Price Of Subscribe"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'value': "",
                'disabled': 'disabled',
            }
        )
    )

    class Meta:
        model = Subscription
        fields = []


class ProjectsSearchForm(forms.Form):
    # name = forms.CharField(
    #     label=_('Name'),
    #     widget=forms.TextInput,
    # )
    # TODO: display form without labels and with placeholders
    type = forms.ChoiceField(
        label=_('Type'),
        choices=Project.TypeList.choices,
        # widget=forms.CheckboxSelectMultiple,
    )
    status = forms.ChoiceField(
        label=_('Status'),
        choices=Project.StatusList.choices,
        # widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].required = False
        self.fields['status'].required = False


class SubPhaseUpdateForm(forms.ModelForm):
    class Meta:
        model = SubPhaseUpdate
        fields = [
            'description',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, }),
        }
