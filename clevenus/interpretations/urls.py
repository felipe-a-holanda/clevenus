from django.conf.urls import patterns, url

from interpretations import views

urlpatterns = patterns('',
  url(r'^$', views.InterpretationList.as_view(), name='interpretation_list'),
  url(r'^new$', views.InterpretationCreate.as_view(), name='interpretation_new'),
  url(r'^edit/(?P<pk>\d+)$', views.InterpretationUpdate.as_view(), name='interpretation_edit'),
  url(r'^delete/(?P<pk>\d+)$', views.InterpretationDelete.as_view(), name='interpretation_delete'),
)
