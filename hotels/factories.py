import factory
from factory.declarations import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger, FuzzyText, FuzzyChoice
from factory.django import ImageField
from accounts.factories import UserFactory
from hotels.models import Feature
from utils.factories import random_subset


class HotelFactory(DjangoModelFactory):
    class Meta:
        model = 'hotels.Hotel'

    name = FuzzyText(prefix='hotel_')
    city = FuzzyText(prefix='city_')
    owner = SubFactory(UserFactory)
    server_url = FuzzyText(prefix='http://server.com/')
    room_count = FuzzyInteger(200)
    stars = FuzzyInteger(1, 5)
    address = FuzzyText()
    is_approved = FuzzyChoice([True, False])

    features = random_subset('features')


class FeatureFactory(DjangoModelFactory):
    class Meta:
        model = 'hotels.Feature'

    name = FuzzyText('f_')
    icon = ImageField()
    is_for_hotel = FuzzyChoice([True, False])
    is_for_room = FuzzyChoice([True, False])


class RoomClassFactory(DjangoModelFactory):
    class Meta:
        model = 'hotels.RoomClass'

    hotel = SubFactory(HotelFactory)
    name = FuzzyText()
    description = FuzzyText()
    price = FuzzyInteger(10000)
    bed_count = FuzzyInteger(3)
    features = random_subset('features')
