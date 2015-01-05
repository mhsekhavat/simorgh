from traceback import print_tb, print_exception
from django.conf import settings
from django.core.management import call_command
import os
from django.db import transaction


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
        # hotel_features = FeatureFactory.create_batch(10, is_for_hotel=True)
        # room_features = FeatureFactory.create_batch(10, is_for_room=True)
        # HotelFactory.create_batch(10, features=hotel_features)
        # RoomClassFactory.create_batch(10)

        from model_mommy import mommy

        import os
        cwd = os.getcwd()
        os.chdir('/tmp/')
        for model in ['auth.User', 'hotels.Feature', 'hotels.Hotel', 'hotels.RoomClass', 'hotels.HotelImage']:
            mommy.make(model, make_m2m=True, _quantity=10)
        os.chdir(cwd)


    gen()
