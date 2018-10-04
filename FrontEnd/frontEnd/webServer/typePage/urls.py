from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^type/$', views.type, name='type'),
    url(r'^type/details/(?P<typeIN>\w{0,50})/$', views.details, name='details'),
    url(r'^type/dllList/(?P<hashIN>\w{0,50})/$', views.dllListings, name='dllListings')
    # url(r'^type/(?P<id>\w{0,50})/$', views.type, name='type')
]
