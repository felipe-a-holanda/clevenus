from django.conf.urls import patterns, include, url
from django.contrib import admin
from astro.views import home

from charts.urls import urlpatterns as chart_urls
from astro.urls import urlpatterns as astro_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'apps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', home),
    url(r'^chart/', include(chart_urls)),
    url(r'^astro/', include(astro_urls)),
    url(r'^user/login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}, name='user-login'),



)
