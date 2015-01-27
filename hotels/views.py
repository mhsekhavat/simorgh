from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from hotels.form import SearchByLocationForm, SearchByNameForm, SearchByVoteForm
from hotels.models import Hotel


def hotels_list(request):
    nameString = request.GET.get('name', '');
    locationString = request.GET.get('location', '');
    votesValue = request.GET.get('votes', -1);
    context = {
        'object_list': Hotel.objects.filter(name__contains=nameString, city__contains=locationString,
                                            stars__gt=votesValue)
    }
    return render_to_response('hotels/hotel_list.html', context)


class HotelUpdate(UpdateView):
    model = Hotel


class HotelView(DetailView):
    model = Hotel
    template_name = 'hotels/hotel_view.html'


class HotelSearchView(TemplateView):
    template_name = 'hotels/hotel_search.html'

    def get_context_data(self, **kwargs):
        return {
            'location_form': SearchByLocationForm(),
            'name_form': SearchByNameForm(),
            'vote_form': SearchByVoteForm()
        }

    def post(self, request):
        return render_to_response()

