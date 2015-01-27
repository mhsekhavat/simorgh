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
    room_class = models.ForeignKey('hotels.RoomClass')
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.PositiveIntegerField()
    room_count = models.PositiveIntegerField()
    status = models.CharField(max_length=32, choices=CHOICES_STATUS)


class Vote(models.Model):
    class Meta:
        ordering = ['releaseDate',]

    user = models.ForeignKey('auth.User')
    reservation_order = models.OneToOneField('reservation.ReservationOrder')
    stars = models.SmallIntegerField(choices=Hotel.CHOICES_STARS)
    comment = models.TextField(blank=True)
    releaseDate = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    followup_code = models.CharField(max_length=255)
    status = models.CharField(max_length=32, choices=ReservationOrder.CHOICES_STATUS)
