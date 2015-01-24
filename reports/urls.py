from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^simorghIncomesByHotels/$', (lambda: None), name='reports_simorgh_incomes_by_hotels'),
    url(r'^simorghTotalIncomse/$', (lambda: None), name='reports_simorgh_total_incomes'),
    url(r'^hotelRoomsIncomes/$', (lambda: None), name='reports_hotel_rooms_incomes'),
    url(r'^hotelDetailedIncomes/$', (lambda: None), name='reports_hotel_detailed_incomes'),
)
