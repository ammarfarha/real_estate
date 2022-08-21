from django import forms
from .models import Project, ProjectImage


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"


class AddProjectImageFileForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = "__all__"


class ProjectsSearchForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'type',
            'statue',
        ]
        labels = {
            'name': '',
            'type': '',
            'statue': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {
                'class': 'col-xs-2',
                'placeholder': 'Name',
             }
        )
        self.fields['name'].required = False
        self.fields['type'].widget.attrs.update()
        self.fields['statue'].widget.attrs.update()
