# -*- coding: utf-8 -*-
from django.forms.forms import Form
from django.forms.fields import CharField
from hotels.models import Hotel
from django import forms

__author__ = 'REAL'


class SearchByLocationForm(Form):
    location = CharField(label=u'نام شهر/استان')


class SearchByNameForm(Form):
    name = CharField(label=u'نام هتل')


class SearchByVoteForm(Form):
    votes = CharField(label=u'رای کاربران')

class UpdateHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        exclude = ('is_approved', )


class RegisterHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('name', 'city', 'server_url', 'room_count', 'stars', 'address', 'features')
