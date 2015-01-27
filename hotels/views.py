# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, FormView, CreateView, ModelFormMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from hotels.form import SearchByLocationForm, SearchByNameForm, SearchByVoteForm, RegisterHotelForm, UpdateHotelForm
from hotels.models import Hotel
from django.contrib import messages


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
    form_class = UpdateHotelForm
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


class HotelRegisterView(CreateView):
    model = Hotel
    template_name = 'hotels/hotel_register.html'
    form_class = RegisterHotelForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        messages.success(self.request, u'هتل جدید با موفقیت ثبت شد، منتظر تایید مدیر سیستم باشید')
        return super(ModelFormMixin, self).form_valid(form)



