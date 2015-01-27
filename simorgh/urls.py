from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
import hotels.urls, accounts.urls, reservation.urls, reports.urls

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'simorgh.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hotels/', include(hotels.urls)),
    url(r'^accounts/', include(accounts.urls)),
    url(r'^reservation/', include(reservation.urls)),
    url(r'^reports/', include(reports.urls)),
)
