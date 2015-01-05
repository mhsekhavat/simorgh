from django.conf.urls import patterns, include, url
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from hotels.models import Hotel

hotel_patterns = patterns(
    '',
    url(r'^$', UpdateView.as_view(model=Hotel), name='hotel_edit'),
)

urlpatterns = patterns(
    '',
    url(r'^$', ListView.as_view(model=Hotel), name='hotel_list'),
    url(r'^(?P<pk>\d+)/', include(hotel_patterns)),
)
