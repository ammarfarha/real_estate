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


# TODO: use forms.Form not ModelForm
class ProjectsSearchForm(forms.Form):
    type = forms.ChoiceField(
        label=_('Type'),
        choices=Project.TypeList.choices,
        widget=forms.CheckboxSelectMultiple,
    )

    # class Meta:
    #     model = Project
    #     fields = [
    #         'name',
    #         'type',
    #         'statue',
    #     ]
    #     labels = {
    #         'name': '',
    #         'type': '',
    #         'statue': '',
    #     }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['name'].widget.attrs.update(
    #         {
    #             'class': 'col-xs-2',
    #             'placeholder': 'Name',
    #         }
    #     )
    #     self.fields['name'].required = False
    #     self.fields['type'].widget.attrs.update()
    #     self.fields['statue'].widget.attrs.update()
