from django import forms
from .models import Project, ProjectImage, Subscription, MainPhase, SubPhase, SubPhaseUpdate, UpdateAttachment
from django.utils.translation import gettext_lazy as _


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'summary',
            'type',
            'location',
            'area',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].required = False

    def clean(self):
        pass


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
