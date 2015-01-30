from django.conf.urls import patterns, include, url
from reports.views import incomes_by_hotels, ReportsView


urlpatterns = patterns(
    '',
    url(r'^$', ReportsView.as_view(), name='reports'),
    url(r'^simorghIncomesByHotels/$', incomes_by_hotels, name='reports_simorgh_incomes_by_hotels'),
    url(r'^simorghTotalIncomse/$', (lambda: None), name='reports_simorgh_total_incomes'),
    url(r'^hotelRoomsIncomes/$', (lambda: None), name='reports_hotel_rooms_incomes'),
    url(r'^hotelDetailedIncomes/$', (lambda: None), name='reports_hotel_detailed_incomes'),
)

