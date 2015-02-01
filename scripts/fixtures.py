# -*- coding: utf-8 -*-
from itertools import cycle
import random
from traceback import print_tb, print_exception
import datetime
import traceback
from django.conf import settings
from django.core.files import File
from django.core.management import call_command
import os
from django.db import transaction
import itertools
from loremipsum.generator import Generator
from hotels.models import Hotel, RoomClass, Feature, HotelImage
from reservation.models import ReservationOrder, Payment, Vote


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

    feature_names = [u'لابی', u'آسانسور', u'لاندری', u'ماهواره', u'وای‌فای', u'آکواریوم', u'دشویی']

    def random_features(is_for_hotel):
        is_for_room = not is_for_hotel
        return random.sample(list(Feature.objects.filter(is_for_hotel=is_for_hotel, is_for_room=is_for_room)), 3)

    def make_features(postfix, is_for_hotel):
        mommy.make_many(
            Feature,
            len(feature_names),
            name=iter(i + postfix for i in feature_names),
            icon=cycle(
                ['http://www.eghamat24.com/images/com/ic_sobhane.png', 'http://www.eghamat24.com/images/com/ic_rest.png']),
            is_for_hotel=is_for_hotel,
            is_for_room=not is_for_hotel,
        )

    make_features(u'هتل', True)
    make_features(u' اتاق', False)

    hotels = mommy.make_many(
        Hotel,
        4,
        name=iter([u'هتل پارسیان', u'هتل هما', u'هتل استقلال', u'هتل امیرکبیر']),
        address=u'نرسیده به آزادی، دانشگاه شریف، دانشکده کامپیوتر، آزمایشگاه طبقه چهارم',
        city=cycle([u'تهران', u'اصفهان']),
        main_image=iter(
            File(open(os.path.join(settings.BASE_DIR, 'images/hotel%d.jpg' % i), 'rb'))
            for i in itertools.count()
        ),
        features=random_features(True),
        owner=iter(users),
    )

    room_classes = []
    for hotel in hotels:
        for i in range(6):
            mommy.make_one(
                HotelImage,
                hotel=hotel,
                caption=u'تصویر %d ام هتل' % i,
                image=File(open(os.path.join(settings.BASE_DIR, 'images/hotel%d.jpg' % i), 'rb')),
            )
        for i in range(3):
            room_class = mommy.make_one(
                RoomClass,
                hotel=hotel,
                name=u'درجه ' + str(i),
                features=random_features(is_for_hotel=False),
                description=lambda: Generator(u'نمتسیب منتسب متشسیبمن شسبمت سیمبنتشسمب سمنب منستیب سنیبتنیب زنرتنسی بنیتبنسبتنس سینبسنتب سنتبنسب سنتعزرههصپثدپ ننزعیت شسمنتبی', u'منتسیب مسشتب مسشبمنسش بمنسشتبمنسش سیب سنبیتس زهعثص زپر نسع منبسشب مسشبنتسشی منبسشمنبشس منبمنسشب'.split()).generate_paragraph()[2],
            )
            room_classes.append(room_class)

    r1 = mommy.make_one(
        ReservationOrder,
        user=users[0],
        room_class=room_classes[0],
        start_date=datetime.datetime(2012, 4, 7),
        end_date=datetime.datetime(2012, 4, 10),
        price=1000000,
        room_count=2,
        status=ReservationOrder.STATUS_PAID
    )

    r2 = mommy.make_one(
        ReservationOrder,
        user=users[2],
        room_class=room_classes[7],
        start_date=datetime.datetime(2012, 8, 10),
        end_date=datetime.datetime(2012, 9, 10),
        price=2500000,
        room_count=3,
        status=ReservationOrder.STATUS_PAID
    )
    r3 = mommy.make_one(
        ReservationOrder,
        user=users[1],
        room_class=room_classes[9],
        start_date=datetime.datetime(2012, 11, 1),
        end_date=datetime.datetime(2013, 12, 2),
        price=3500000,
        room_count=2,
        status=ReservationOrder.STATUS_PAID
    )

    r4 = mommy.make_one(
        ReservationOrder,
        user=users[3],
        room_class=room_classes[11],
        start_date=datetime.datetime(2012, 1, 1),
        end_date=datetime.datetime(2013, 5, 2),
        price=360000,
        room_count=2,
        status=ReservationOrder.STATUS_WAITING
    )

    r5 = mommy.make_one(
        ReservationOrder,
        user=users[4],
        room_class=room_classes[5],
        start_date=datetime.datetime(2012, 1, 1),
        end_date=datetime.datetime(2012, 5, 2),
        price=500000,
        room_count=2,
        status=ReservationOrder.STATUS_EXPIRED
    )

    r6 = mommy.make_one(
        ReservationOrder,
        room_class=room_classes[3],
        user=users[3],
        start_date=datetime.datetime(2011, 1, 1),
        end_date=datetime.datetime(2012, 5, 2),
        price=1500000,
        room_count=4,
        status=ReservationOrder.STATUS_PAID
    )

    peymants = mommy.make_many(
        Payment,
        10,
        status=cycle(iter(ReservationOrder.CHOICES_STATUS))
    )

    votes = mommy.make_many(
        Vote,
        6,
        reservation_order=iter([r1, r2, r3, r4, r5, r6]),
        stars=cycle(iter([1, 2, 2, 2, 3, 4, 5])),
        comment=cycle(['خوب بود ممون', 'افتضاح بود']),
        release_date=cycle(iter(
            [datetime.datetime(2012, 2, 6), datetime.datetime(2013, 5, 7), datetime.datetime(2012, 11, 20),
             datetime.datetime(2010, 7, 26)]))
    )

    os.chdir(cwd)


def run():
    try:
        os.remove(settings.DATABASES['default']['NAME'])
        call_command('migrate')
        gen()
    except OSError:
        pass
    except Exception:
        traceback.print_exc()
