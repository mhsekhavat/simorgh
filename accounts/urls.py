from django.conf.urls import patterns, include, url
from accounts import views

urlpatterns = patterns(
    '',
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
)
