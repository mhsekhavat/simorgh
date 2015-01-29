# -*- coding: utf-8 -*-
from django.forms.forms import Form
from django.forms.fields import CharField
from hotels.models import Hotel, HotelImage
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
        exclude = ('is_approved', 'owner')

    def __init__(self, *args, **kwargs):
        super(UpdateHotelForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['address'].widget.attrs['rows'] = 3


class HotelAddImageForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        exclude = ('hotel', )

    def __init__(self, *args, **kwargs):
        super(HotelAddImageForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['caption'].widget.attrs['rows'] = 1


class RegisterHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('name', 'city', 'server_url', 'room_count', 'stars', 'address', 'features')

    def __init__(self, *args, **kwargs):
        super(RegisterHotelForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['address'].widget.attrs['rows'] = 3
