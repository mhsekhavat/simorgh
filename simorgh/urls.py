from django.conf.urls import patterns, include, url
from django.contrib import admin
import hotels.urls
from hotels.views import HotelsList

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'simorgh.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^hotels/', include(hotels.urls)),
)
