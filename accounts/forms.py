# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.tests.custom_user import CustomUserNonUniqueUsername
from django.forms.models import fields_for_model, model_to_dict
from models import UserProfile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label=u'گذرواژه')
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phoneNumber',)


class UserProfileEditForm(forms.ModelForm):
    def __init__(self, instance=None, initial=None, *args, **kwargs):
        _fields = ('first_name', 'last_name', 'email')
        _initial = model_to_dict(instance.user, _fields) if instance is not None else {}
        super(UserProfileEditForm, self).__init__(initial=_initial, instance=instance, *args, **kwargs)
        self.fields.update(fields_for_model(User, _fields))

    class Meta:
        model = UserProfile
        exclude = ('user', 'activation_key', 'key_expires', )

    new_password = forms.CharField(widget=forms.PasswordInput, required=False, label=u'گذرواژه‌ی جدید', help_text=u'اگر نیاز به تغییر گذرواژه ندارید، این قسمت را خالی بگذارید')

    def save(self, *args, **kwargs):
        u = self.instance.user
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.email = self.cleaned_data['email']
        new_password = self.cleaned_data['new_password']
        if new_password:
            u.set_password(new_password)
        u.save()
        profile = super(UserProfileEditForm, self).save(*args,**kwargs)
        return profile

    def has_changed_password(self):
        return self.cleaned_data['new_password'] != ''

    #nam nameKHanevadegi adress email password

