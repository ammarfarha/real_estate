from datetime import datetime
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
    user = models.OneToOneField(User,
                                related_name="client",
                                null=False,
                                blank=False,
                                on_delete=models.CASCADE
                                )
    birth_date = models.DateField(null=True,
                                  blank=False,
                                  verbose_name=_('Birth Date')
                                  )
    phone = models.CharField(max_length=12,
                             null=True,
                             blank=False,
                             verbose_name=_('Phone Number')
                             )  # need to change to phone field
    mobile = models.CharField(max_length=12,
                              null=True,
                              blank=False,
                              verbose_name=_('Mobile Number')
                              )  # need to change to phone field
    nationality = CountryField(verbose_name=_('Country'),
                               default='BH',
                               null=True,
                               blank=False
                               )
    gender = models.CharField(max_length=2,
                              verbose_name=_('Gender'),
                              choices=GenderList.choices,
                              default=GenderList.MALE,
                              null=True,
                              blank=False
                              )
    city = models.CharField(max_length=200,
                            verbose_name=_('City'),
                            null=True,
                            blank=False
                            )
    address = models.TextField(verbose_name=_('Full Address'),
                               null=True,
                               blank=False
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
    is_company = models.BooleanField(default=False,
                                     verbose_name=_('Are you a Company?')
                                     )
    company_name = models.CharField(max_length=300,
                                    unique=True,
                                    db_index=True,
                                    verbose_name=_('Company Name'),
                                    null=True,
                                    blank=True
                                    )
    web_site = models.URLField(max_length=400,
                               unique=True,
                               verbose_name=_('Company Website'),
                               null=True,
                               blank=True
                               )
    trade_record = models.FileField(verbose_name=_('Trade Record'),
                                    null=True,
                                    blank=True
                                    )

    # meta:
    # srt:
    def __str__(self):
        return str(self.user)
    # clean:
    # save:

