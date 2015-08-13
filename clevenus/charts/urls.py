from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'date/(\d*-\d*-\d*)/(\d*:\d*)/', chartDate),
    url(r'date/(\d*-\d*-\d*)/', chartDate),
    url(r'post', postIntepretation),
    url(r'(?P<chart_id>\d*)', chartView),

)