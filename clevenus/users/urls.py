from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'(?P<username>[\w-]+)', user_profile_view, name='user-profile'),

)