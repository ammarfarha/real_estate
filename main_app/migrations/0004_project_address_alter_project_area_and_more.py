# Generated by Django 4.1 on 2022-09-03 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_subphaseupdate_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='address',
            field=models.CharField(blank=True, max_length=600, null=True, verbose_name='Project Address'),
        ),
        migrations.AlterField(
            model_name='project',
            name='area',
            field=models.DecimalField(decimal_places=0, max_digits=10, null=True, verbose_name='Area in Square Meters'),
        ),
        migrations.AlterField(
            model_name='subphase',
            name='completion_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Actual Completion Date'),
        ),
        migrations.AlterField(
            model_name='subphase',
            name='end_date',
            field=models.DateField(null=True, verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='subphase',
            name='phase',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_phases', to='main_app.mainphase', verbose_name='Main Phase'),
        ),
        migrations.AlterField(
            model_name='subphaseupdate',
            name='description',
            field=models.TextField(null=True, verbose_name='Update Description'),
        ),
    ]