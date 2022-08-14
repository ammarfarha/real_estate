from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models

admin.site.register(models.Developer)
admin.site.register(models.Client, UserAdmin)
