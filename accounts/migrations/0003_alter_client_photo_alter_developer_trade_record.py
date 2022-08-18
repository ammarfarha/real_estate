# Generated by Django 4.1 on 2022-08-18 22:27

import accounts.file_validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_client_options_alter_developer_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='photo',
            field=models.ImageField(null=True, upload_to='photos/', verbose_name='Client Photo'),
        ),
        migrations.AlterField(
            model_name='developer',
            name='trade_record',
            field=models.FileField(blank=True, null=True, upload_to='treads/', validators=[accounts.file_validator.validate_file_extentions], verbose_name='Trade Record'),
        ),
    ]
