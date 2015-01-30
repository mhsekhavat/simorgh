# -*- coding: utf-8 -*-
from django.db import models
from hotels.models import Hotel


class ReservationOrder(models.Model):
    STATUS_WAITING = 'waiting'
    STATUS_PAID = 'paid'
    STATUS_EXPIRED = 'expired'
    CHOICES_STATUS = (
        (STATUS_WAITING, 'در انتظار پرداخت'),
        (STATUS_PAID, 'پرداخت شده'),
        (STATUS_EXPIRED, 'منقضی'),
    )
    user = models.ForeignKey('auth.User', verbose_name=u'کاربر')
    room_class = models.ForeignKey('hotels.RoomClass', verbose_name=u'رده‌بندی اتاق')
    start_date = models.DateField(verbose_name=u'تاریخ شروع')
    end_date = models.DateField(verbose_name=u'تاریخ پایان')
    price = models.PositiveIntegerField(verbose_name=u'قیمت')
    room_count = models.PositiveIntegerField(verbose_name=u'تعداد اتاق')
    status = models.CharField(max_length=32, choices=CHOICES_STATUS, verbose_name=u'وضعیت پرداخت')


class Vote(models.Model):
    class Meta:
        ordering = ['releaseDate',]

    reservation_order = models.OneToOneField('reservation.ReservationOrder', verbose_name=u'رسید پرداخت')
    stars = models.SmallIntegerField(choices=Hotel.CHOICES_STARS, verbose_name=u'ستاره')
    comment = models.TextField(blank=True, verbose_name=u'نظر')
    releaseDate = models.DateTimeField(auto_now_add=True, verbose_name=u'تاریخ انتشار')


class Payment(models.Model):
    followup_code = models.CharField(max_length=255, verbose_name=u'کد پیگیری')
    status = models.CharField(max_length=32, choices=ReservationOrder.CHOICES_STATUS, verbose_name=u'وضعیت پرداخت')
