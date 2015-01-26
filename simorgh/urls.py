from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.sitemaps import Sitemap, GenericSitemap
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from hotels.models import Hotel
import hotels.urls, accounts.urls, reservation.urls, reports.urls
from hotels.views import HotelsList
from django.contrib.sitemaps.views import sitemap


class StaticViewsSitemap(Sitemap):
    def items(self):
        return ['home', 'hotel_list', 'login', 'register', 'accounts_edit', 'confirm', 'hotel_list', 'hotel_view',
                'hotel_search', 'hotel_new']

    def location(self, obj):
        return reverse(obj)


sitemaps = {
    'static': StaticViewsSitemap,
    'hotels': GenericSitemap(dict(queryset=Hotel.objects.all()))
}

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'simorgh.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hotels/', include(hotels.urls)),
    url(r'^accounts/', include(accounts.urls)),
    url(r'^reservation/', include(reservation.urls)),
    url(r'^reports/', include(reports.urls)),
)
