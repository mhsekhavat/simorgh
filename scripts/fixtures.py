# -*- coding: utf-8 -*-
import random
from traceback import print_tb, print_exception
import datetime
from django.conf import settings
from django.core.management import call_command
import os
from django.db import transaction
from hotels.models import Hotel, RoomClass, Feature
from reservation.models import ReservationOrder


@transaction.atomic()
def gen():
    # UserFactory.create_batch(10)
    # hotel_feature_names = FeatureFactory.create_batch(10, is_for_hotel=True)
    # room_features = FeatureFactory.create_batch(10, is_for_room=True)
    # HotelFactory.create_batch(10, features=hotel_feature_names)
    # RoomClassFactory.create_batch(10)

    from model_mommy import mommy

    import os

    cwd = os.getcwd()
    os.chdir('/tmp/')
    from django.contrib.auth.models import User

    PASSWORD = 'admin'
    admin = User.objects.create_superuser(
        username='admin',
        password=PASSWORD,
        email='a@b.com',
    )

    names = [u'علی', u'تقی', u'نقی', u'سجاد', u'رضا']
    users = [
        User.objects.create_user(
            username=('user%i' % i),
            password=PASSWORD,
            email='email@gmail.com',
            first_name=names[i],
            last_name=names[i] + u'یان',
        ) for i in range(5)
    ]

    hotels = mommy.make_many(
        Hotel,
        2,
        name=iter([u'هتل پارسیان', u'هتل هما', ]),
        owner=iter(users),
    )

    feature_names = [u'لابی', u'آسانسور', u'لاندری', u'ماهواره', u'وای‌فای', u'آکواریوم', u'دشویی']
    mommy.make_many(
        Feature,
        len(feature_names),
        name=iter(feature_names),
        is_for_hotel=True,
        is_for_room=False,
    )

    mommy.make_many(
        Feature,
        len(feature_names),
        name=iter(feature_names),
        is_for_hotel=False,
        is_for_room=True,
    )


    def random_features(is_for_hotel):
        is_for_room = not is_for_hotel
        return random.sample(list(Feature.objects.filter(is_for_hotel=is_for_hotel, is_for_room=is_for_room)), 3)

    room_classes = []
    for hotel in hotels:
        for i in range(3):
            room_class = mommy.make_one(
                RoomClass,
                hotel=hotel,
                name=u'درجه ' + str(i),
                features=random_features(is_for_hotel=False)
            )
            room_classes.append(room_class)

    r1 = mommy.make_one(
        ReservationOrder,
        room_class=room_classes[0],
        start_date=datetime.datetime(2012, 4, 7),
        end_date=datetime.datetime(2012, 4, 10),
        price=1000000,
        room_count=2,
        status=ReservationOrder.STATUS_PAID
    )

    r2 = mommy.make_one(
        ReservationOrder,
        room_class=room_classes[1],
        start_date=datetime.datetime(2012, 8, 10),
        end_date=datetime.datetime(2012, 9, 10),
        price=2500000,
        room_count=3,
        status=ReservationOrder.STATUS_PAID
    )
    r3 = mommy.make_one(
        ReservationOrder,
        room_class=room_classes[2],
        start_date=datetime.datetime(2012, 11, 1),
        end_date=datetime.datetime(2013, 12, 2),
        price=3500000,
        room_count=2,
        status=ReservationOrder.STATUS_PAID
    )

    r4 = mommy.make_one(
        ReservationOrder,
        room_class=room_classes[1],
        start_date=datetime.datetime(2012, 1, 1),
        end_date=datetime.datetime(2013, 5, 2),
        price=360000,
        room_count=2,
        status=ReservationOrder.STATUS_WAITING
    )

    r5 = mommy.make_one(
        ReservationOrder,
        room_class=room_classes[3],
        start_date=datetime.datetime(2012, 1, 1),
        end_date=datetime.datetime(2012, 5, 2),
        price=500000,
        room_count=2,
        status=ReservationOrder.STATUS_EXPIRED
    )

    r6 = mommy.make_one(
        ReservationOrder,
        room_class=room_classes[2],
        start_date=datetime.datetime(2011, 1, 1),
        end_date=datetime.datetime(2012, 5, 2),
        price=1500000,
        room_count=4,
        status=ReservationOrder.STATUS_EXPIRED
    )

    p1
    os.chdir(cwd)


def run():
    try:
        os.remove(settings.DATABASES['default']['NAME'])
        call_command('migrate')
        gen()
    except OSError:
        pass
