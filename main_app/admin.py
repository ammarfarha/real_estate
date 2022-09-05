from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from . import models

admin.site.register(models.Project, LeafletGeoAdmin)
admin.site.register(models.Subscription)
admin.site.register(models.MainPhase)
admin.site.register(models.SubPhase)
admin.site.register(models.SubPhaseUpdate)
admin.site.register(models.UpdateAttachment)
admin.site.register(models.ProjectImage)
