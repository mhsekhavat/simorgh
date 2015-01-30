from django.shortcuts import render, render_to_response



# Create your views here.
from mercurial.commands import status
from hotels.models import Hotel
from reservation.models import ReservationOrder


def incomes_by_hotels(re):
    hotel_incomes = {}
    reservation_orders = ReservationOrder.objects.filter(status=ReservationOrder.STATUS_PAID, start_date__gte='2000-1-1',
                                           end_date__lte='2020-1-1')
    for reservation_order in reservation_orders:
        hotel = reservation_order.room_class.hotel
        hotel_incomes.setdefault(hotel, 0)
        hotel_incomes[hotel] += reservation_order.price

    hotels = []
    for hotel in Hotel.objects.all():
        hotels.append({
            'hotel': hotel,
            'income': hotel_incomes.get(hotel, 0),
        })

    context = {
        'hotels': hotels
    }

    return render_to_response('reports/report_hotels_income.html', context)


