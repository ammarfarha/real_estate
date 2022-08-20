# Generated by Django 4.1 on 2022-08-19 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainPhase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Title')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=300, null=True, verbose_name='Project Name')),
                ('summary', models.TextField(max_length=300, null=True, verbose_name='Summary')),
                ('type', models.CharField(choices=[('CO', 'Commercial'), ('RE', 'Residential'), ('IN', 'Industrial'), ('SP', 'Special Purpose'), ('LA', 'Lands')], default='CO', max_length=2, null=True, verbose_name='Type of the Project')),
                ('statue', models.CharField(choices=[('PL', 'Planing'), ('IN', 'Initial'), ('UC', 'Under Construction'), ('DO', 'Done'), ('RE', 'Ready To Use')], default='PL', max_length=2, null=True, verbose_name='The project Status')),
                ('location', models.TextField(null=True, verbose_name='Location')),
                ('area', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Area in Square Meters')),
                ('stakeholders', models.TextField(blank=True, null=True, verbose_name='Project Stakeholders')),
                ('neighborhood', models.TextField(blank=True, null=True, verbose_name='Project Neighborhood')),
                ('developer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='accounts.developer', verbose_name='Developer')),
            ],
        ),
        migrations.CreateModel(
            name='SubPhase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Title')),
                ('start_date', models.DateField(null=True, verbose_name='Start Date')),
                ('end_date', models.DateField(null=True, verbose_name='Finish Date')),
                ('completion_date', models.DateTimeField(null=True, verbose_name='Duration')),
                ('phase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_phases', to='main_app.mainphase', verbose_name='Sub Phase')),
            ],
        ),
        migrations.CreateModel(
            name='SubPhaseUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_date', models.DateField(auto_now_add=True, verbose_name='Update Date')),
                ('description', models.TextField(null=True, verbose_name='Update Description')),
                ('sub_phase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_phases_update', to='main_app.subphase', verbose_name='Sub Phase Update')),
            ],
        ),
        migrations.CreateModel(
            name='UpdateAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_file', models.FileField(blank=True, null=True, upload_to='', verbose_name='Attachment')),
                ('update', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='update_sub_phases', to='main_app.subphaseupdate', verbose_name='Update Sun Phase')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_date', models.DateField(auto_now_add=True, verbose_name='Subscription Date')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='Client')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='main_app.project', verbose_name='Project')),
                ('referral_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions_by', to=settings.AUTH_USER_MODEL, verbose_name='Referral User')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='projects/', verbose_name='Client Photo')),
                ('alt', models.CharField(max_length=200, null=True)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_images', to='main_app.project', verbose_name='Project')),
            ],
        ),
        migrations.AddField(
            model_name='mainphase',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_phases', to='main_app.project', verbose_name='Project'),
        ),
    ]
