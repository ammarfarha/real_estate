from django import forms
from leaflet.forms.fields import PointField

from .models import Project, ProjectImage, Subscription, MainPhase, SubPhase, SubPhaseUpdate, UpdateAttachment
from django.utils.translation import gettext_lazy as _
from leaflet.forms.widgets import LeafletWidget


class AddProjectForm(forms.ModelForm):
    location = PointField(
        required=True,
        widget=LeafletWidget(
            attrs={
                'display_raw': True,
                'map_width': '600px',
                'map_height': '400px',
            }
        ))

    class Meta:
        model = Project
        fields = [
            'name',
            'summary',
            'type',
            'area',
        ]


class AddProjectImageFileForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = [
            'image',
            'alt',
        ]


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = [
            'referral_user',
        ]


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
