from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^status/$', (lambda: None), name='reservation_status'),
    url(r'^pay/$', (lambda: None), name='reservation_pay'),
    url(r'^finalApprove/$', (lambda: None), name='reservation_final_approve'),
    url(r'^vacher/$', (lambda: None), name='reservation_vacher'),
    url(r'^list/$', (lambda: None), name='reservation_list'),
)
