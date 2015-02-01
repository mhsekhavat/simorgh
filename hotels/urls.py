from django.conf.urls import patterns, include, url
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import BaseDetailView
from hotels.models import Hotel
from hotels.views import HotelSearchView, HotelUpdate, HotelView, hotels_list, HotelRegisterView, HotelAddImageView, HotelRemoveImage, HotelAddRoomClass, HotelEditRoomClass, HotelRemoveRoomClass, HotelListAdmin

hotel_patterns = patterns(
    '',
    url(r'^update/$', HotelUpdate.as_view(), name='hotel_edit'),
    url(r'^update/addImage$', HotelAddImageView.as_view(), name='hotel_add_image'),
    url(r'^update/addRoomClass$', HotelAddRoomClass.as_view(), name='hotel_add_room_class'),
    url(r'^update/editRoomClass/(?P<room_class_pk>\d+)/$', HotelEditRoomClass.as_view(), name='hotel_edit_room_class'),
    url(r'^update/removeRoomClass/(?P<room_class_pk>\d+)/$', HotelRemoveRoomClass.as_view(),
        name='hotel_delete_room_class'),
    url(r'^update/removeImage/(?P<images_pk>\d+)/$', HotelRemoveImage.as_view(), name='hotel_remove_image'),
    url(r'^view/$', HotelView.as_view(), name='hotel_view'),
    # url(r'^data.map/$', GeoJSONLayerView.as_view(model=Hotel), name='data'),
)

urlpatterns = patterns(
    '',
    url(r'^$', hotels_list, name='hotel_list'),
    url(r'^admin/$', HotelListAdmin.as_view(), name='hotel_list_admin'),
    url(r'^search/$', HotelSearchView.as_view(), name='hotel_search'),
    url(r'^(?P<pk>\d+)/', include(hotel_patterns)),
    url(r'^roomClass/$', (lambda: None), name='hotel_room_class_edit'),
    url(r'^new/$', HotelRegisterView.as_view(), name='hotel_new'),
    url(r'^approve/$', (lambda: None), name='hotel_approve'),
)
