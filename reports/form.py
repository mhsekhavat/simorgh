# -*- coding: utf-8 -*-
from django.forms.fields import CharField, DateField
from django.forms.forms import Form


class DateSelectForm(Form):
    hotel_incomes_start_date=DateField(label=u'تاریخ شروع گزارش‌گیری')
    hotel_incomes_end_date=DateField(label=u'تاریخ پایان گزارش‌گیری')
