from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _


class GenderList(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')


class Client(models.Model):
    # Constants:
    # Fields:
    user = models.OneToOneField(
        User,
        related_name="client",
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    birth_date = models.DateField(
        null=True,
        blank=False,
        verbose_name=_('Birth Date')
    )
    # TODO: need to change to phone field
    phone = models.CharField(
        max_length=12,
        null=True,
        blank=False,
        verbose_name=_('Phone Number')
    )
    # TODO: need to change to phone field
    mobile = models.CharField(
        max_length=12,
        null=True,
        blank=False,
        verbose_name=_('Mobile Number')
    )
    nationality = CountryField(
        verbose_name=_('Country'),
        default='BH',
        null=True,
        blank=False,
    )
    gender = models.CharField(
        max_length=2,
        verbose_name=_('Gender'),
        choices=GenderList.choices,
        default=GenderList.MALE,
        null=True,
        blank=False
    )
    city = models.CharField(
        max_length=200,
        verbose_name=_('City'),
        null=True,
        blank=False
    )
    address = models.TextField(
        verbose_name=_('Full Address'),
        null=True,
        blank=False
    )
    photo = models.ImageField(
        verbose_name=_('Client Photo'),
        null=True,
        blank=False,
    )

    # meta:
    # srt:
    def __str__(self):
        return str(self.user)
    # clean:
    # save:


class Developer(Client):
    # Constants:
    # Fields:
    is_company = models.BooleanField(
        default=False,
        verbose_name=_('Are you a Company?')
    )
    company_name = models.CharField(
        max_length=300,
        unique=True,
        db_index=True,
        verbose_name=_('Company Name'),
        null=True,
        blank=True
    )
    web_site = models.URLField(
        max_length=400,
        unique=True,
        verbose_name=_('Company Website'),
        null=True,
        blank=True
    )
    trade_record = models.FileField(
        verbose_name=_('Trade Record'),
        null=True,
        blank=True
    )

    # meta:
    # srt:
    # str:
    # clean:
    # save:


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
        return self.name + " - developed by: (" + str(self.developer) + ")"
    # clean:
    # save:


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
        User,
        related_name='subscriptions',
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
        return self.title + " in: " + str(self.project)
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
        return self.title + "  - of -  " + str(self.phase)
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
