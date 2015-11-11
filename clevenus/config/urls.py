from django.conf.urls import patterns, include, url
from django.contrib import admin
from astro.views import home
from django.conf import settings
from charts.urls import urlpatterns as chart_urls
from astro.urls import urlpatterns as astro_urls
from users.urls import urlpatterns as user_urls
from api.urls import urlpatterns as api_urls
from interpretations.urls import urlpatterns as interpretations_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'apps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    url(r'^chart/', include(chart_urls)),
    url(r'^interpretation/', include(interpretations_urls)),


    url(r'^astro/', include(astro_urls)),

    #url(r'^user/login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}, name='user-login'),
    url(r'^user/', include(user_urls)),
    url(r'^api/', include(api_urls)),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))