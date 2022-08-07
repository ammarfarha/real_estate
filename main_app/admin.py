from django.contrib import admin
from .models import (
    Client,
    Developer,
    )

admin.site.register(Client)
admin.site.register(Developer)
