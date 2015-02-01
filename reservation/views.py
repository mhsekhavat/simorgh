# -*- coding: utf-8 -*-
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.edit import FormView


class StatusView(FormView):
    def post(self, request, *args, **kwargs):
        return HttpResponse(u'ظرفیت: ' + 10)
