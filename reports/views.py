from django.shortcuts import render, render_to_response



# Create your views here.
from django.views.generic.base import TemplateView
#from mercurial.commands import status
from hotels.models import Hotel
from reports.form import DateSelectForm
from reservation.models import ReservationOrder


def incomes_by_hotels(request):
    hotel_incomes_start_date = request.GET.get('hotel_incomes_start_date', '1900-1-1')
    hotel_incomes_end_date = request.GET.get('hotel_incomes_end_date', '2100-1-1')
    hotel_incomes = {}
    reservation_orders = ReservationOrder.objects.filter(status=ReservationOrder.STATUS_PAID,
                                                         start_date__gte=hotel_incomes_start_date,
                                                         end_date__lte=hotel_incomes_end_date)
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

def incomes_by_hotels(request):
    #hotel_incomes_start_date = request.GET.get('hotel_incomes_start_date', '1900-1-1')
    #hotel_incomes_end_date = request.GET.get('hotel_incomes_end_date', '2100-1-1')
    form = DateSelectForm(data=request.GET)
    if form.is_valid():
        hotel_incomes_start_date = form.cleaned_data.get('hotel_incomes_start_date', None)
        hotel_incomes_end_date = form.cleaned_data.get('hotel_incomes_end_date', None)

    hotel_incomes = {}
    reservation_orders = ReservationOrder.objects.filter(status=ReservationOrder.STATUS_PAID,
                                                         start_date__gte=hotel_incomes_start_date,
                                                         end_date__lte=hotel_incomes_end_date)
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




class ReportsView(TemplateView):
    template_name = 'reports/reports.html'

    def get_context_data(self, **kwargs):
        # hotel_incomes_start_date=self.request.GET.get('hotel_incomes_start_date','1900-1-1')
        # hotel_incomes_end_date=self.request.GET.get('hotel_incomes_end_date','2100-1-1')
        return {
            'hotels_incomes': DateSelectForm(),
            'total_incomes' : DateSelectForm(),
            'hotel_rooms_incomes' : DateSelectForm(),
            'hotel_detailed_incomes' : DateSelectForm(),
        }



