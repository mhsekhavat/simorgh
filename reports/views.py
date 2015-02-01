from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY
from django.shortcuts import render, render_to_response


# Create your views here.
from django.views.generic.base import TemplateView
# from mercurial.commands import status
from hotels.models import Hotel, RoomClass
from reports.form import DateSelectForm
from reservation.models import ReservationOrder


def incomes_by_hotels(request):
    incomes_start_date = request.GET.get('incomes_start_date', '1900-1-1')
    incomes_end_date = request.GET.get('incomes_end_date', '2100-1-1')
    hotel_incomes = {}
    reservation_orders = ReservationOrder.objects.filter(status=ReservationOrder.STATUS_PAID,
                                                         start_date__gte=incomes_start_date,
                                                         end_date__lte=incomes_end_date)
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


def total_incomes(request):
    form = DateSelectForm(data=request.GET)
    if form.is_valid():
        incomes_start_date = form.cleaned_data.get('incomes_start_date', None)
        incomes_end_date = form.cleaned_data.get('incomes_end_date', None)

    monthly_incomes = {}
    reservation_orders = ReservationOrder.objects.filter(status=ReservationOrder.STATUS_PAID,
                                                         start_date__gte=incomes_start_date,
                                                         end_date__lte=incomes_end_date)

    for dt in rrule(MONTHLY, dtstart=incomes_start_date, until=incomes_end_date):
        for reservation_order in reservation_orders:
            if dt.date() < reservation_order.start_date and (
                        dt + relativedelta(months=1) ).date() > reservation_order.start_date:
                monthly_incomes.setdefault(dt.strftime('%Y-%m'), 0)
                monthly_incomes[dt.strftime('%Y-%m')] += reservation_order.price

    months = []
    for dt in rrule(MONTHLY, dtstart=incomes_start_date, until=incomes_end_date):
        months.append({
            'date': dt.strftime('%Y-%m'),
            'income': monthly_incomes.get(dt.strftime('%Y-%m'), 0),
        })

    context = {
        'months': months
    }

    return render_to_response('reports/report_total_income.html', context)


def incomes_by_hotel_rooms(request):
    incomes_start_date = request.GET.get('incomes_start_date', '1900-1-1')
    incomes_end_date = request.GET.get('incomes_end_date', '2100-1-1')
    rooms_incomes = {}
    reservation_orders = ReservationOrder.objects.filter(status=ReservationOrder.STATUS_PAID,
                                                         start_date__gte=incomes_start_date,
                                                         end_date__lte=incomes_end_date)
    for reservation_order in reservation_orders:
        if reservation_order.room_class.hotel.owner.username == request.user.username:
            rooms_incomes.setdefault(reservation_order.room_class, 0)
            rooms_incomes[reservation_order.room_class] += reservation_order.price

    rooms = []
    for room in RoomClass.objects.all():
        if rooms_incomes.get(room, 0) > 0:
            rooms.append({
                'room': room,
                'income': rooms_incomes.get(room, 0),
            })

    context = {
        'rooms': rooms
    }

    return render_to_response('reports/report_hotel_rooms_income.html', context)


def detailed_incomes(request):
    incomes_start_date = request.GET.get('incomes_start_date', '1900-1-1')
    incomes_end_date = request.GET.get('incomes_end_date', '2100-1-1')
    reservation_detailed = {}
    reservation_orders = ReservationOrder.objects.filter(start_date__gte=incomes_start_date,
                                                         end_date__lte=incomes_end_date)
    for reservation_order in reservation_orders:
        if reservation_order.room_class.hotel.owner.username == request.user.username:
            reservation_detailed.setdefault(
                    reservation_order.room_class.name + "  " + reservation_order.user.username + "  " + reservation_order.status + "  " + reservation_order.start_date.strftime(
                        "%Y-%m-%d") + "  " + reservation_order.start_date.strftime("%Y-%m-%d"), 0)
            reservation_detailed[
                reservation_order.room_class.name + "  " + reservation_order.user.username + "  " + reservation_order.status + "  " + reservation_order.start_date.strftime(
                    "%Y-%m-%d") + "  " + reservation_order.start_date.strftime("%Y-%m-%d")] += reservation_order.price

            orders = []
            for reserve in reservation_detailed.keys():
                orders.append({
                    'order': reserve,
                    'income': reservation_detailed.get(reserve, 0),
                })

            context = {
                'orders': orders
            }

    return render_to_response('reports/report_hotel_detailed_income.html', context)


class ReportsView(TemplateView):
    template_name = 'reports/reports.html'

    def get_context_data(self, **kwargs):
        # hotel_incomes_start_date=self.request.GET.get('hotel_incomes_start_date','1900-1-1')
        # hotel_incomes_end_date=self.request.GET.get('hotel_incomes_end_date','2100-1-1')
        return {
            'select_date': DateSelectForm(),
        }



