from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = [
    url(r'^v1.0/', include([
        url(r'^get_data/(.*)/(.*)/$', get_data, name='api-aspect'),
    ])),

]