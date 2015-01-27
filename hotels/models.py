from django.core.urlresolvers import reverse_lazy
from django.db import models
import datetime

class Hotel(models.Model):
    CHOICES_STARS = [(i, u'%d Stars' % i) for i in range(1, 6)]
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=56, blank=True)
    owner = models.ForeignKey('auth.User')
    server_url = models.URLField(blank=True)
    room_count = models.PositiveIntegerField()
    stars = models.SmallIntegerField(choices=CHOICES_STARS)
    address = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    features = models.ManyToManyField('hotels.Feature', blank=True)

    def vote_set(self):
        #stars = []
        #comments = []
        #for room_class in self.roomclass_set.all():
        #    for reservation_order in room_class.reservationorder_set.all():
        #        stars.append(reservation_order.vote.stars)

        from reservation.models import Vote
        #for vote in Vote.objects.filter(reservation_order__hotel=self):
            #stars.append(vote.stars)
            #comments.append(vote.comment)
        return Vote.objects.filter(reservation_order__hotel=self)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('hotel_edit', kwargs={'pk': self.id})


class RoomClass(models.Model):
    hotel = models.ForeignKey('hotels.Hotel')
    name = models.CharField(max_length=32)
    description = models.TextField()
    price = models.PositiveIntegerField()
    bed_count = models.PositiveIntegerField()
    features = models.ManyToManyField('hotels.Feature')

    def __unicode__(self):
        return self.name


class HotelImage(models.Model):
    hotel = models.ForeignKey('hotels.Hotel')
    caption = models.TextField(blank=True)
    image = models.ImageField()

    def __unicode__(self):
        return self.caption


class Feature(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField()
    is_for_hotel = models.BooleanField(default=True)
    is_for_room = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
