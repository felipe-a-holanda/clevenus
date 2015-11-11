from django.conf.urls import patterns, include, url

from .views import *

urlpatterns = patterns('',
    url(r'^$', UserListView.as_view(), name='user-list'),

    url(r'^create/(?P<pk>[\d]+)/', UserCreate.as_view(), name='userprofile-view'),
    url(r'^register/', SignUp.as_view(), name='register'),
    url(r'(?P<username>[\w-]+)', user_profile_view, name='user-profile'),

)