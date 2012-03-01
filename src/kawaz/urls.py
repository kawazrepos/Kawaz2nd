from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls'), name='admin_doc'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^registration/', include('registration.urls')),
    # core
    url(r'^members/', include('kawaz.core.profiles.urls')),
    # api
    url(r'^api/profiles/', include('kawaz.core.profiles.api.urls')),
)
