# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Malware, Dlltable, Malware2Dll
from django.contrib import admin


admin.site.register(Malware)
admin.site.register(Dlltable)
admin.site.register(Malware2Dll)
