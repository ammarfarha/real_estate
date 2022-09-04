from django.db import models
from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site Name', null=True, blank=True)
    maintenance_mode = models.BooleanField(default=False)
    projects_phases_template = models.TextField(null=True, blank=True)

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
