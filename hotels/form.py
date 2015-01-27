# -*- coding: utf-8 -*-
from django.forms.forms import Form
from django.forms.fields import CharField

__author__ = 'REAL'


class SearchByLocationForm(Form):
    location = CharField(label=u'نام شهر/استان')


class SearchByNameForm(Form):
    name = CharField(label=u'نام هتل')


class SearchByVoteForm(Form):
    votes = CharField(label=u'رای کاربران')

