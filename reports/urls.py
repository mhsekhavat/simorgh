from django.conf.urls import patterns, include, url
from reports.views import incomes_by_hotels, ReportsView, total_incomes, detailed_incomes, incomes_by_hotel_rooms


urlpatterns = patterns(
    '',
    url(r'^$', ReportsView.as_view(), name='reports'),
    url(r'^simorghIncomesByHotels/$', incomes_by_hotels, name='reports_simorgh_incomes_by_hotels'),
    url(r'^simorghTotalIncomse/$', total_incomes, name='reports_simorgh_total_incomes'),
    url(r'^hotelRoomsIncomes/$', incomes_by_hotel_rooms, name='reports_hotel_rooms_incomes'),
    url(r'^hotelDetailedIncomes/$', detailed_incomes, name='reports_hotel_detailed_incomes'),
)

