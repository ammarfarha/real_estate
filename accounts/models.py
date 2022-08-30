from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from .file_validator import validate_file_extensions
from phonenumber_field.modelfields import PhoneNumberField
from .utils import generate_ref_code


class GenderList(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')


class Client(AbstractUser):
    birth_date = models.DateField(null=True, blank=False, verbose_name=_('Birth Date'))
    phone = PhoneNumberField(
        # max_length=12,
        null=True,
        blank=False,
        verbose_name=_('Phone Number')
    )
    mobile = PhoneNumberField(
        # max_length=12,
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
        blank=True,
    )
    photo = models.ImageField(
        verbose_name=_('Client Photo'),
        null=True,
        blank=True,
        upload_to='photos/',
    )
    code = models.CharField(
        max_length=20,
        verbose_name=_('Code'),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = 'Clients'

    # srt:
    def __str__(self):
        if self.first_name and self.last_name:
            return str(self.first_name) + " " + str(self.last_name)
        return str(self.username)

    def get_developer(self):
        developer = Developer.objects.filter(username=self.username)
        return developer.first()

    def is_developer(self):
        return bool(self.get_developer())

    def get_logo_image_or_avatar(self):
        if self.photo:
            return self.photo.url
        else:
            return '{}{}'.format(settings.STATIC_URL, 'images/avatar.png')

    def save(self, *args, **kwargs):
        if self.code == "":
            self.code = generate_ref_code()

        super().save(*args, **kwargs)


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
        validators=[validate_file_extensions],
    )

    # super.is_active =
    class Meta:
        verbose_name = _('Developer')
        verbose_name_plural = 'Developers'

    def __str__(self):
        return str(self.username)
    # clean:
    # save:
