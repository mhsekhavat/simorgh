from django.conf.urls import patterns, include, url
from accounts import views

urlpatterns = patterns(
    '',
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^confirm/(?P<activation_key>\w+)/', ('accounts.views.register_confirm')),
    url(r'^edit/$', views.AccountsEdit.as_view(), name='accounts_edit'),
)
