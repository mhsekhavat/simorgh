from django.shortcuts import render, render_to_response



# Create your views here.
from hotels.models import Hotel


def incomes_by_hotels(re):
    context={
        'object_list':Hotel.objects.all()
    }
    return render_to_response('reports/report_hotels_income.html', context)


