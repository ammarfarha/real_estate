# Generated by Django 4.1 on 2022-09-01 18:27

import martor.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0002_alter_subscription_referral_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subphaseupdate',
            name='description',
            field=martor.models.MartorField(null=True, verbose_name='Update Description'),
        ),
    ]
