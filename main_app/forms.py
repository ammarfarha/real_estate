from django import forms
from .models import Project, ProjectImage


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"


class addProjectImageFileForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = "__all__"
