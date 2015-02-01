# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template.context import RequestContext
from django.views.generic import View
from django.views.generic.edit import UpdateView
from accounts.forms import UserForm, UserProfileForm, UserProfileEditForm
from accounts.models import UserProfile
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib import messages
import hashlib, datetime, random
from hotels.models import Hotel


def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request, u'حساب کاربری شما غیرفعال می‌باشد.')
                return render_to_response('accounts/accounts_login.html', {}, context)
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            messages.error(request, u'نام کاربری یا رمز عبور اشتباه می‌باشد.')
            return render_to_response('accounts/accounts_login.html', {}, context)
    else:
        return render_to_response('accounts/accounts_login.html', {}, context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)

            user.is_active = False

            username = user.username
            email = user.email
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt + email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.activation_key = activation_key
            profile.key_expires = key_expires

            profile.save()

            registered = True

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours http://127.0.0.1:8000/accounts/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'simorgh@gmail.com',
                      [email], fail_silently=False)

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
        'accounts/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)


def register_confirm(request, activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/home')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        messages.error(request, u'مدت اعتبار لینک به پایان رسیده است')
        return HttpResponseRedirect('/', {})

    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    messages.info(request, u'حساب کاربری شما فعال گردید')
    return HttpResponseRedirect('/')

class AccountsEdit(UpdateView):
    template_name = 'accounts/accounts_edit.html'
    model = UserProfile
    form_class = UserProfileEditForm
    changed_password = False
    def get_object(self, queryset=None):
        user_profile,created = UserProfile.objects.get_or_create(user=self.request.user);
        return user_profile

    def form_valid(self, form):
        if form.has_changed_password():
            self.changed_password = True
            messages.success(self.request, u'رمز عبور شما با موفقیت تغییر کرد. لطفا دوباره وارد شوید')
        else:
            messages.success(self.request, u'حساب کاربری شما با موفقیت به روزرسانی شد')
        return super(AccountsEdit, self).form_valid(form)

    def get_success_url(self):
        if( self.changed_password ):
            return '/'
        else:
            return reverse_lazy('accounts_edit')


class HotelPermissionMixin(View):
    editing = True

    def dispatch(self, request, *args, **kwargs):
        try:
            hotel = Hotel.objects.get(id=kwargs['pk'])
        except Hotel.DoesNotExist:
            raise Http404()
        if self.editing:
            if not hotel.has_edit_permission():
                raise SuspiciousOperation()
        return super(HotelPermissionMixin, self).dispatch(request, *args, **kwargs)


class SuperUserMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_super_user:
            raise SuspiciousOperation()
        return super(SuperUserMixin, self).dispatch(request, *args, **kwargs)
