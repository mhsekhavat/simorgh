from django.contrib import admin
from hotels.models import Hotel, RoomClass, HotelImage

admin.site.register(Hotel)
admin.site.register(RoomClass)
admin.site.register(HotelImage)