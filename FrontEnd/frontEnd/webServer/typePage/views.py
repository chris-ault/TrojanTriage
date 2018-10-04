# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from .models import Malware, Element
from django.shortcuts import render
from django.db.models import Count


def index(request):
    return HttpResponse('Hello')


def type(request):
    # q = Malware.objects.values('type').distinct()
    # type = Element.objects.values('type').distinct()
    # typec = Element.objects.values('type').distinct().count()
    count = Element.objects.values('type').annotate(
        total=Count('type')).order_by('-total')

    # This context Dictionary Carries the QuerySet count as a value to the 'type' key
    # the context is then passed to the page processor? for viewing
    context = {
        'type': count
    }
    return render(request, 'types.html', context)


def details(request, typeIN):
    q = Element.objects.filter(type=typeIN).order_by('-severity')
    print q.query
    context = {
        'hash': q
    }
    return render(request, 'detailList.html', context)
