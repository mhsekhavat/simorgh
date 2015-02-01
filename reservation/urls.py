from django.conf.urls import patterns, include, url
from reservation.views import StatusView

roomclass_patterns = patterns(
    '',
    url(r'^status/$', StatusView.as_view(), name='reservation_status'),
)

urlpatterns = patterns(
    '',
    url(r'^(?P<pk>\d+)/', include(roomclass_patterns)),
    url(r'^pay/$', (lambda: None), name='reservation_pay'),
    url(r'^finalApprove/$', (lambda: None), name='reservation_final_approve'),
    url(r'^vacher/$', (lambda: None), name='reservation_vacher'),
    url(r'^list/$', (lambda: None), name='reservation_list'),
)
