from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from .file_validator import validate_file_extentions


class GenderList(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')


class Client(AbstractUser):
    birth_date = models.DateField(null=True, blank=False, verbose_name=_('Birth Date'))
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
        blank=False,
    )
    city = models.CharField(
        max_length=200,
        verbose_name=_('City'),
        null=True,
        blank=False,
    )
    address = models.TextField(
        verbose_name=_('Full Address'),
        null=True,
        blank=False,
    )
    photo = models.ImageField(
        verbose_name=_('Client Photo'),
        null=True,
        blank=False,
        upload_to='photos/',
    )

    class Meta:
        verbose_name = 'Client'  # TODO: translated
        verbose_name_plural = 'Clients'

    # srt:
    def __str__(self):
        return "client : " + str(self.username)
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
        blank=True,
        upload_to='treads/',
        validators=[validate_file_extentions],
        # TODO: allowed file types extensions
    )

    class Meta:
        verbose_name = 'Developer'
        verbose_name_plural = 'Developers'

    def __str__(self):
        return "dev : " + str(self.username)
    # clean:
    # save:
