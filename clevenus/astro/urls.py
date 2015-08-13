from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'search/$', search_view, name='search'),
    url(r'planet/(?P<planet>\w+)/$', planet_view, name='planet-view'),
    url(r'sign/(?P<sign>\w+)/$', sign_view, name='sign-view'),
    url(r'house/(?P<house>\w+)/$', house_view, name='house-view'),
    url(r'planet-in-sign/(?P<planet>\w+)/(?P<sign>\w+)/$', planet_in_sign, name='planet-in-sign'),
    url(r'house-in-sign/(?P<house>\w+)/(?P<sign>\w+)/$', house_in_sign, name='house-in-sign'),
    url(r'planet-in-house/(?P<planet>\w+)/(?P<house>\w+)/$', planet_in_house, name='planet-in-house'),
    url(r'aspect/(?P<planet1>\w+)/(?P<aspect_type>\w+)/(?P<planet2>\w+)/$', aspect, name='aspect'),
)