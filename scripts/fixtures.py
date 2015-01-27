# -*- coding: utf-8 -*-
import random
from traceback import print_tb, print_exception
from django.conf import settings
from django.core.management import call_command
import os
from django.db import transaction
from hotels.models import Hotel, RoomClass, Feature


def run():
    try:
        os.remove(settings.DATABASES['default']['NAME'])
        call_command('migrate')
    except OSError:
        pass
    # -*- coding: utf-8 -*-
    # from accounts.factories import UserFactory
    # from hotels.factories import HotelFactory
    # from hotels.factories import FeatureFactory, RoomClassFactory
    # from hotels.models import Hotel

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


        for hotel in hotels:
            for i in range(3):
                room_class = mommy.make_one(
                    RoomClass,
                    hotel=hotel,
                    name=u'درجه ' + str(i),
                    features=random_features(is_for_hotel=False)
                )

        os.chdir(cwd)


    gen()
