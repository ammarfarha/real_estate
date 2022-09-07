from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from djgeojson.fields import PointField
from geopy.geocoders import Nominatim

from accounts.models import Developer, Client
from shared_app.models import SiteConfiguration


# TODO: use the below manager in all pages facing the client
class VisibleProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(visibility=Project.Visibility.PUBLISHED)


class Project(models.Model):
    # Constants:
    class TypeList(models.TextChoices):
        COMMERCIAL = 'CO', _('Commercial')
        RESIDENTIAL = 'RE', _('Residential')
        INDUSTRIAL = 'IN', _('Industrial')
        SPECIAL_PURPOSE = 'SP', _('Special Purpose')
        LANDS = 'LA', _('Lands')

    class StatusList(models.TextChoices):
        PLANNING = 'PL', _('Planning')
        INITIAL = 'IN', _('Initial')
        UNDER_CONSTRUCTION = 'UC', _('Under Construction')
        DONE = 'DO', _('Done')
        READY_TO_USE = 'RE', _('Ready To Use')

    class Visibility(models.TextChoices):
        UNDER_REVIEW = 'UR', _('Under Review')
        PUBLISHED = 'P', _('Published')
        HIDDEN_BY_DEVELOPER = 'HD', _('Hidden by the Developer')
        HIDDEN_BY_ADMIN = 'HA', _('Hidden by he Admin')

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
        verbose_name=_('Type'),
        default=TypeList.COMMERCIAL,
        null=True,
        blank=False,
    )
    statue = models.CharField(
        max_length=2,
        choices=StatusList.choices,
        verbose_name=_('Status'),
        default=StatusList.PLANNING,
        null=True,
        blank=False,
    )
    visibility = models.CharField(
        max_length=2,
        choices=Visibility.choices,
        verbose_name=_('Visibility'),
        default=Visibility.UNDER_REVIEW,
        null=True,
        blank=False,
    )
    location = PointField()
    area = models.DecimalField(
        verbose_name=_('Area (Square Meters)'),
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=False,
    )

    objects = models.Manager()
    visible_projects = VisibleProjectManager()

    def __str__(self):
        return str(self.name)

    def get_first_image_or_default(self):
        if self.project_images.all():
            return self.project_images.all().first().image.url
        else:
            return '{}{}'.format(settings.STATIC_URL, 'images/no_image.jpg')

    def can_edit(self, developer):
        return self.developer == developer

    def can_subscribe(self, client):
        return client.is_authenticated and not bool(
            self.subscriptions.all().filter(client=client)) and not self.can_edit(client)

    def is_subscribed(self, client):
        return client.is_authenticated and self.subscriptions.filter(client=client).exists()

    # region geolocator methods
    def _get_reversed_geolocator(self, language='ar'):
        if self.location and self.location.get("coordinates"):
            geolocator = Nominatim(user_agent="main_app")
            return geolocator.reverse(reversed(self.location["coordinates"]), language=language, addressdetails=True)

    def address(self, language='ar'):
        project_address = self._get_reversed_geolocator(language)
        return str(project_address) if project_address else _('No address')

    def _get_address_component(self, component, language='ar'):
        project_address = self._get_reversed_geolocator(language)
        if project_address and project_address.raw:
            address_components = project_address.raw.get('address')
            if address_components and address_components.get(component):
                return address_components.get(component)

        return ''

    def country(self):
        language = translation.get_language()
        return self._get_address_component(component='country', language=language)

    def country_code(self):
        language = translation.get_language()
        return self._get_address_component(component='country_code', language=language)

    def state(self):
        language = translation.get_language()
        return self._get_address_component(component='state', language=language)

    def province(self):
        language = translation.get_language()
        return self._get_address_component(component='province', language=language)

    def suburb(self):
        language = translation.get_language()
        return self._get_address_component(component='suburb', language=language)
    # endregion geolocator methods

    def visible(self):
        return self.visibility == Project.Visibility.PUBLISHED

    def create_main_and_sub_phases_from_template(self):
        config = SiteConfiguration.get_solo()
        projects_phases_template = config.projects_phases_template
        if projects_phases_template:
            lines = projects_phases_template.splitlines()

            if lines[0].startswith('****'):
                raise Exception('Invalid Phases Template in Site Configurations. Kindly contact the site admin.')

            current_main_phase, current_sub_phase, main_phase_list, sub_phase_list = None, None, [], []
            for line in lines:
                if line.startswith('***'):
                    sub_phase_list.append(SubPhase(title=line.replace('***', ''), phase=current_main_phase))
                else:
                    current_main_phase = MainPhase(title=line, project=self)
                    main_phase_list.append(current_main_phase)

            MainPhase.objects.bulk_create(main_phase_list)
            SubPhase.objects.bulk_create(sub_phase_list)

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
        blank=True,
    )

    # meta:
    # srt:
    def __str__(self):
        return str(self.client) + " - subscribe in: " + str(self.project)
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

    # clean:
    # save:


class SubPhase(models.Model):
    # Constants:
    # Fields:
    phase = models.ForeignKey(
        MainPhase,
        related_name='sub_phases',
        verbose_name=_('Main Phase'),
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
        verbose_name=_('End Date'),
        null=True,
        blank=False,
    )
    completion_date = models.DateTimeField(
        verbose_name=_('Actual Completion Date'),
        null=True,
        blank=True,
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
        related_name='updates',
        verbose_name=_('Sub Phase Update'),
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    # TODO: change to datetime
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
        related_name='attachments',
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
