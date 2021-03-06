# -*- coding: utf-8 -*-
from django.forms.forms import Form
from django.forms.fields import CharField
from django.forms.models import ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from hotels.models import Hotel, HotelImage, RoomClass, Feature
from django import forms


class SearchByLocationForm(Form):
    location = CharField(label=u'نام شهر/استان')


class SearchByNameForm(Form):
    name = CharField(label=u'نام هتل')


class SearchByVoteForm(Form):
    votes = CharField(label=u'رای کاربران')


class UpdateHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        exclude = ('is_approved', 'owner')

    features = ModelMultipleChoiceField(widget=CheckboxSelectMultiple(),
                                        queryset=Feature.objects.filter(is_for_hotel=True))

    def __init__(self, *args, **kwargs):
        super(UpdateHotelForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['address'].widget.attrs['rows'] = 3


def feature_field(**filter):
    return ModelMultipleChoiceField(widget=CheckboxSelectMultiple(),
                                    queryset=Feature.objects.filter(**filter))


class UpdateRoomClassForm(forms.ModelForm):
    class Meta:
        model = RoomClass
        exclude = ('hotel', )

    features = feature_field(is_for_room=True)


    # def __init__(self, *args, **kwargs):
    # super(UpdateRoomClassForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
    # self.fields['description'].widget.attrs['rows'] = 3


class HotelAddImageForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        exclude = ('hotel', )

    def __init__(self, *args, **kwargs):
        super(HotelAddImageForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['caption'].widget.attrs['rows'] = 1


class HotelAddRoomClass(forms.ModelForm):
    class Meta:
        model = RoomClass
        exclude = ('hotel', )

    def __init__(self, *args, **kwargs):
        super(HotelAddRoomClass, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['description'].widget.attrs['rows'] = 1


class RegisterHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('name', 'city', 'server_url', 'room_count', 'stars', 'address', 'features')

    features = feature_field(is_for_hotel=True)

    def __init__(self, *args, **kwargs):
        super(RegisterHotelForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['address'].widget.attrs['rows'] = 3


class StatusForm(forms.Form):
    start_date = forms.DateField(label=u'از تاریخ')
    end_date = forms.DateField(label=u'تا تاریخ')
