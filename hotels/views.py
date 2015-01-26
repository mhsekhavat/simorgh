from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from hotels.form import SearchByLocationForm, SearchByNameForm, SearchByVoteForm
from hotels.models import Hotel


class HotelsList(ListView):
    model = Hotel
    template_name = 'hotels/hotel_list.html'


class HotelUpdate(UpdateView):
    model = Hotel


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