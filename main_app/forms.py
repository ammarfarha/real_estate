from django import forms
from leaflet.forms.fields import PointField

from .models import Project, ProjectImage, Subscription, MainPhase, SubPhase, SubPhaseUpdate, UpdateAttachment
from django.utils.translation import gettext_lazy as _
from leaflet.forms.widgets import LeafletWidget


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

    def __init__(self, * args, **kwargs):
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

    def __init__(self, * args, **kwargs):
        super().__init__(*args, **kwargs)


class SubscriptionForm(forms.ModelForm):
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
            'description': forms.Textarea(attrs={'rows': 3,}),
        }
