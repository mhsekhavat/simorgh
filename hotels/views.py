from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from hotels.models import Hotel


class HotelsList(ListView):
    model = Hotel
    template_name = 'hotels/hotel_list.html'


class HotelUpdate(UpdateView):
    model = Hotel

