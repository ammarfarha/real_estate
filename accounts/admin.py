from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from .forms import ClientCreationForm, DeveloperCreationForm


class ClientAdmin(UserAdmin):
    model = models.Client
    add_form = ClientCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
    )


class DeveloperAdmin(UserAdmin):
    model = models.Developer
    add_form = DeveloperCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
    )


admin.site.register(models.Developer, DeveloperAdmin)
admin.site.register(models.Client, ClientAdmin)
