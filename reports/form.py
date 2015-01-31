# -*- coding: utf-8 -*-
from django.forms.fields import CharField, DateField
from django.forms.forms import Form


class DateSelectForm(Form):
    incomes_start_date=DateField(label=u'تاریخ شروع گزارش‌گیری')
    incomes_end_date=DateField(label=u'تاریخ پایان گزارش‌گیری')
