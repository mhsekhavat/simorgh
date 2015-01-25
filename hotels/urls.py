from django.conf.urls import patterns, include, url
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from hotels.models import Hotel
from hotels.views import HotelSearchView

hotel_patterns = patterns(
    '',
    url(r'^$', UpdateView.as_view(model=Hotel), name='hotel_edit'),
)

urlpatterns = patterns(
    '',
    url(r'^$', ListView.as_view(model=Hotel), name='hotel_list'),
    url(r'^search/$', HotelSearchView.as_view(), name='hotel_search'),
    url(r'^(?P<pk>\d+)/', include(hotel_patterns)),
    url(r'^view/$', (lambda: None), name='hotel_view'),
    url(r'^search/$', (lambda: None), name='hotel_search'),
    url(r'^roomClass/$', (lambda: None), name='hotel_room_class_edit'),
    url(r'^new/$', (lambda: None), name='hotel_new'),
    url(r'^approve/$', (lambda: None), name='hotel_approve'),
)
