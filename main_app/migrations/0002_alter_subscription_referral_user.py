# Generated by Django 4.1 on 2022-08-30 21:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='referral_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='subscriptions_by', to=settings.AUTH_USER_MODEL,
                                    verbose_name='Referral User'),
        ),
    ]
