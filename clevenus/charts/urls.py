from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^date/(\d*-\d*-\d*)/(\d*:\d*)/(.*)/$', chartDate, name="chart_date_time_location"),
    url(r'^date/(\d*-\d*-\d*)/(\d*:\d*:\d*)/(.*)/$', chartDate, name="chart_date_times_location"),
    url(r'^date/(\d*-\d*-\d*/\d*:\d*)/$', chartDate, name="chart_datetime"),
    url(r'^date/(\d*-\d*-\d*)/(\d*:\d*)/$', chartDate, name="chart_date_time"),
    url(r'^date/(\d*-\d*-\d*)/(\d*:\d*:\d*)/$', chartDate, name="chart_date_times"),
    url(r'^date/(\d*-\d*-\d*)/$', chartDate, name="chart_date"),
    url(r'^post/$', postIntepretation),
    url(r'^events/$', EventListView.as_view(), name='event-list'),
    url(r'^(?P<username>\w*)/$', chartView, name='chart-view'),
    url(r'^(?P<username>\w*)/transits/$', transits, name='transits-view'),

)