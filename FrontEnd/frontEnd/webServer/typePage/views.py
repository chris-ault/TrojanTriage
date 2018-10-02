# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from .models import Malware, Element

from django.shortcuts import render


def index(request):
    return HttpResponse('Hello')

def type(request):
    #q = Malware.objects.values('type').distinct()
    type = Element.objects.values('type').distinct()
    # Would be nice to pass a count(type) parameter into this for quantity of each
    context = {
        'type': type
    }
    return render(request, 'types.html', context)


def details(request, typeIN):
    q = Element.objects.filter(type = typeIN)
    print q
    context = {
        'hash': q
    }
    return render(request, 'detailList.html', context)
