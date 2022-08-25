from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from accounts.models import Developer, Client


class Project(models.Model):
    # Constants:
    class TypeList(models.TextChoices):
        COMMERCIAL = 'CO', _('Commercial')
        RESIDENTIAL = 'RE', _('Residential')
        INDUSTRIAL = 'IN', _('Industrial')
        SPECIAL_PURPOSE = 'SP', _('Special Purpose')
        LANDS = 'LA', _('Lands')

    class StatusList(models.TextChoices):
        PLANING = 'PL', _('Planing')
        INITIAL = 'IN', _('Initial')
        UNDER_CONSTRUCTION = 'UC', _('Under Construction')
        DONE = 'DO', _('Done')
        READY_TO_USE = 'RE', _('Ready To Use')

    # Fields:
    developer = models.ForeignKey(
        Developer,
        related_name='projects',
        verbose_name=_('Developer'),
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        blank=False,
    )
    name = models.CharField(
        max_length=300,
        verbose_name=_('Project Name'),
        db_index=True,
        null=True,
        blank=False
    )
    summary = models.TextField(
        max_length=300,
        verbose_name=_('Summary'),
        null=True,
        blank=False,
    )
    type = models.CharField(
        max_length=2,
        choices=TypeList.choices,
        verbose_name=_('Type of the Project'),
        default=TypeList.COMMERCIAL,
        null=True,
        blank=False,
    )
    statue = models.CharField(
        max_length=2,
        choices=StatusList.choices,
        verbose_name=_('The project Status'),
        default=StatusList.PLANING,
        null=True,
        blank=False,
    )
    location = models.TextField(
        verbose_name=_('Location'),
        null=True,
        blank=False
    )
    area = models.DecimalField(
        verbose_name=_('Area in Square Meters'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=False,
    )
    stakeholders = models.TextField(
        verbose_name=_('Project Stakeholders'),
        null=True,
        blank=True
    )
    neighborhood = models.TextField(
        verbose_name=_('Project Neighborhood'),
        null=True,
        blank=True
    )

    # meta:
    # srt:
    def __str__(self):
        return str(self.name)

    def get_first_image_or_default(self):
        if self.project_images.all():
            return self.project_images.all().first().image.url
        else:
            return '{}{}'.format(settings.STATIC_URL, 'images/no_image.jpg')

    def can_edit(self, developer):
        return developer.username == Developer.objects.filter(pk=self.developer_id).first().username

    def can_subscribe(self, client):
        return not bool(self.subscriptions.all().filter(client=client)) and not self.can_edit(client)

    # clean:
    # save:


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        related_name='project_images',
        verbose_name=_('Project'),
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    image = models.ImageField(
        verbose_name=_('Client Photo'),
        null=True,
        blank=False,
        upload_to='projects/',
    )
    alt = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )


class Subscription(models.Model):
    # Constants:
    # Fields:
    client = models.ForeignKey(
        Client,
        related_name='subscriptions',
        verbose_name=_('Client'),
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    project = models.ForeignKey(
        Project,
        related_name='subscriptions',
        verbose_name=_('Project'),
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    subscription_date = models.DateField(
        auto_now_add=True,
        verbose_name=_('Subscription Date')
    )
    referral_user = models.ForeignKey(
        Client,
        related_name='subscriptions_by',
        verbose_name=_('Referral User'),
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )

    # meta:
    # srt:
    def __str__(self):
        return str(self.client) + " - subscripe in: " + str(self.project)
    # clean:
    # save:


class MainPhase(models.Model):
    # Constants:
    # Fields:
    project = models.ForeignKey(
        Project,
        related_name='main_phases',
        verbose_name=_('Project'),
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    title = models.CharField(
        max_length=500,
        verbose_name=_('Title'),
        null=True,
        blank=False,
    )

    # meta:
    # srt:
    def __str__(self):
        return str(self.title)

    def get_sub_phases_or_none(self):
        return self.sub_phases.all()
    # clean:
    # save:


class SubPhase(models.Model):
    # Constants:
    # Fields:
    phase = models.ForeignKey(
        MainPhase,
        related_name='sub_phases',
        verbose_name=_('Sub Phase'),
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    title = models.CharField(
        max_length=500,
        verbose_name=_('Title'),
        null=True,
        blank=False,
    )
    start_date = models.DateField(
        verbose_name=_('Start Date'),
        null=True,
        blank=False,
    )
    end_date = models.DateField(
        verbose_name=_('Finish Date'),
        null=True,
        blank=False,
    )
    completion_date = models.DateTimeField(
        verbose_name=_('Duration'),
        null=True,
        blank=False,
    )

    # meta:
    # srt:
    def __str__(self):
        return str(self.title)
    # clean:
    # save:


class SubPhaseUpdate(models.Model):
    # Constants:
    # Fields:
    sub_phase = models.ForeignKey(
        SubPhase,
        related_name='sub_phases_update',
        verbose_name=_('Sub Phase Update'),
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    update_date = models.DateField(
        verbose_name=_('Update Date'),
        auto_now_add=True,
    )
    description = models.TextField(
        verbose_name=_('Update Description'),
        null=True,
        blank=False,
    )

    # meta:
    # srt:
    def __str__(self):
        return "Update " + str(self.sub_phase) + " where " + str(self.description)
    # clean:
    # save:


class UpdateAttachment(models.Model):
    # Constants:
    # Fields:
    update = models.ForeignKey(
        SubPhaseUpdate,
        related_name='update_sub_phases',
        verbose_name=_('Update Sun Phase'),
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    update_file = models.FileField(
        verbose_name=_('Attachment'),
        null=True,
        blank=True,
    )

    # meta:
    # srt:
    def __str__(self):
        return "File for: " + str(self.update)
    # clean:
    # save:
