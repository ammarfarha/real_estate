from django.contrib import admin
from . import models

admin.site.register(models.Project)
admin.site.register(models.Subscription)
admin.site.register(models.MainPhase)
admin.site.register(models.SubPhase)
admin.site.register(models.SubPhaseUpdate)
admin.site.register(models.UpdateAttachment)
admin.site.register(models.ProjectImage)
admin.site.register(models.Message)