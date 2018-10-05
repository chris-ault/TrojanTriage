# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from .models import Malware, Element, Dlltable, Malware2Dll
from django.shortcuts import render
from django.db.models import Count


def index(request):
    return HttpResponse('Hello')


def type(request):
    # typec = Element.objects.values('type').distinct().count()
    # count = Element.objects.all().values('type').annotate(total=Count('type'))
    count = Malware.objects.values('type').annotate(
        total=Count('type')).order_by('-total')

    # This context Dictionary Carries the QuerySet count as a value to the 'type' key
    # the context is then passed to the page processor? for viewing
    context = {
        'type': count
    }
    return render(request, 'types.html', context)


def details(request, typeIN):
    q = Malware.objects.filter(type=typeIN).order_by('-severity')
    print q.query
    context = {
        'hash': q
    }
    return render(request, 'detailList.html', context)

# Raw query filter, order_by and values available here
# https://stackoverflow.com/a/43454799/10434952
def dllListings(request, hashIN):
    # q = Dlltable.objects.filter(Malware2Dll__malware_dll_id).values('dll_name')
    # p = Malware2Dll.objects.filter(hash=hashIN).values('malware_dll_id')
    # q = Dlltable.objects.select_related('malware_dll_id').filter(Malware2Dll.hash=hashIN)

    # After Many Attempts I gave in
    q = Dlltable.objects.raw('SELECT dll_name from dlltable d INNER JOIN '
                             'malware2dll m on d.malware_dll_id = m.malware_dll_id '
                             'where hash = %s', [hashIN])
    context = {
        'dllName': q
    }
    return render(request, 'dllList.html', context)
