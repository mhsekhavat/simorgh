# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, ModelFormMixin, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.shortcuts import redirect

from accounts.views import HotelPermissionMixin, SuperUserMixin
from hotels.form import SearchByLocationForm, SearchByNameForm, SearchByVoteForm, RegisterHotelForm, UpdateHotelForm, \
    HotelAddImageForm, HotelAddRoomClass, UpdateRoomClassForm, \
    StatusForm
from hotels.models import Hotel, HotelImage, RoomClass


class HotelList(ListView):
    model = Hotel
    template_name = 'hotels/hotel_list.html'

    def get_context_data(self, **kwargs):
        nameString = self.request.GET.get('name', '')
        locationString = self.request.GET.get('location', '')
        votesValue = self.request.GET.get('votes', -1)

        return {'object_list': filter(Hotel.has_edit_permission,
                                      Hotel.all.filter(name__contains=nameString, city__contains=locationString,
                                                       stars__gt=votesValue))}


class HotelListAdmin(SuperUserMixin, ListView):
    model = Hotel
    template_name = 'hotels/hotel_list_admin.html'

    def get_context_data(self, **kwargs):
        return {'object_list': Hotel.all.filter()}


    def post(self, request, *args, **kwargs):
        list_post = request.POST.getlist('toupdate')
        hotels = Hotel.all.filter()
        for hotel in hotels:
            if hotel.is_approved:
                if list_post.count(str(hotel.id)) == 0:
                    hotel.is_approved = False
                    hotel.save()
            else:
                if list_post.count(str(hotel.id)) != 0:
                    hotel.is_approved = True
                    hotel.save()
        return redirect(reverse_lazy('hotel_list_admin'))


class HotelUpdate(HotelPermissionMixin, UpdateView):
    form_class = UpdateHotelForm
    model = Hotel
    template_name = 'hotels/hotel_edit.html'


class HotelAddImageView(HotelPermissionMixin, CreateView):
    form_class = HotelAddImageForm
    model = HotelImage
    template_name = 'hotels/hotel_add_image.html'
    # success_url = reverse_lazy('hotel_update')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.hotel_id = self.kwargs['pk']
        object.save()
        messages.success(self.request, u'عکس با موفقیت اضافه شد.')
        return redirect(reverse_lazy('hotel_edit', kwargs=self.kwargs))


class HotelRemoveImage(HotelPermissionMixin, DeleteView):
    model = HotelImage

    def get_success_url(self):
        return reverse_lazy('hotel_edit', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        messages.info(self.request, u'عکس با موفقیت حذف شد')
        return HotelImage.objects.get(pk=self.kwargs['images_pk'])


class HotelAddRoomClass(HotelPermissionMixin, CreateView):
    model = RoomClass
    form_class = HotelAddRoomClass
    template_name = 'hotels/hotel_add_room_class.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.hotel_id = self.kwargs['pk']
        object.save()
        messages.success(self.request, u'کلاس اتاق با موفقیت اضافه شد')
        return redirect(reverse_lazy('hotel_edit', kwargs=self.kwargs))


class HotelEditRoomClass(HotelPermissionMixin, UpdateView):
    model = RoomClass
    form_class = UpdateRoomClassForm
    template_name = 'hotels/hotel_edit_room_class.html'

    def get_success_url(self):
        messages.info(self.request, u'ویرایش کلاس اتاق با موفقیت انجام شد')
        return reverse_lazy('hotel_edit', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        return RoomClass.objects.get(pk=self.kwargs['room_class_pk'])


class HotelRemoveRoomClass(HotelPermissionMixin, DeleteView):
    model = RoomClass

    def get_success_url(self):
        return reverse_lazy('hotel_edit', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        messages.info(self.request, u'کلاس اتاق با موفقیت حذف شد')
        return RoomClass.objects.get(pk=self.kwargs['room_class_pk'])


class HotelView(HotelPermissionMixin, DetailView):
    model = Hotel
    template_name = 'hotels/hotel_view.html'
    editing = False

    def get_context_data(self, **kwargs):
        ret = super(HotelView, self).get_context_data(**kwargs)
        ret['estelam_form'] = StatusForm()
        return ret


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



