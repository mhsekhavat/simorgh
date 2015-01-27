# -*- coding: utf-8 -*-
from django.forms.forms import Form
from django.forms.fields import CharField

__author__ = 'REAL'


class SearchByLocationForm(Form):
    name = CharField(label=u'نام شهر/استان')


class SearchByNameForm(Form):
    name = CharField(label=u'نام هتل')


class SearchByVoteForm(Form):
    name = CharField(label=u'رای کاربران')

