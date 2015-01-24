# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phoneNumber = models.CharField(validators=[phone_regex], blank=True, max_length=40, verbose_name=u'شماره تلفن');

    def __unicode__(self):
        return self.user.username
