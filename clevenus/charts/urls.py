from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'post', postIntepretation),
    url(r'(?P<chart_id>\d*)', chartView),

)