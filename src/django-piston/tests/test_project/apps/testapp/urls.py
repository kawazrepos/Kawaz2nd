from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication, DjangoAuthentication

from test_project.apps.testapp.handlers import (EntryHandler, ExpressiveHandler,
                                                AbstractHandler, EchoHandler,
                                                PlainOldObjectHandler,
                                                Issue58Handler,
                                                ListFieldsHandler)

basic_auth = HttpBasicAuthentication(realm='TestApplication')
django_auth = DjangoAuthentication()

basic_auth_entries = Resource(handler=EntryHandler, authentication=basic_auth)
basic_auth_expressive = Resource(handler=ExpressiveHandler, authentication=basic_auth)
basic_auth_abstract = Resource(handler=AbstractHandler, authentication=basic_auth)

django_auth_entries = Resource(handler=EntryHandler, authentication=django_auth)
django_auth_expressive = Resource(handler=ExpressiveHandler, authentication=django_auth)
django_auth_abstract = Resource(handler=AbstractHandler, authentication=django_auth)

echo = Resource(handler=EchoHandler)
popo = Resource(handler=PlainOldObjectHandler)
list_fields = Resource(handler=ListFieldsHandler)
issue58 = Resource(handler=Issue58Handler)

urlpatterns = patterns('',
    url(r'^basic_auth/entries/$', basic_auth_entries),
    url(r'^basic_auth/entries/(?P<pk>.+)/$', basic_auth_entries),
    url(r'^basic_auth/entries\.(?P<emitter_format>.+)', basic_auth_entries),
    url(r'^basic_auth/entry-(?P<pk>.+)\.(?P<emitter_format>.+)', basic_auth_entries),
    
    url(r'^django_auth/entries/$', django_auth_entries),
    url(r'^django_auth/django_auth_entries/(?P<pk>.+)/$', django_auth_entries),
    url(r'^django_auth/django_auth_entries\.(?P<emitter_format>.+)', django_auth_entries),
    url(r'^django_auth/entry-(?P<pk>.+)\.(?P<emitter_format>.+)', django_auth_entries),   

    url(r'^issue58\.(?P<emitter_format>.+)$', issue58),

    url(r'^basic_auth/expressive\.(?P<emitter_format>.+)$', basic_auth_expressive),

    url(r'^basic_auth/abstract\.(?P<emitter_format>.+)$', basic_auth_abstract),
    url(r'^basic_auth/abstract/(?P<id_>\d+)\.(?P<emitter_format>.+)$', basic_auth_abstract),

    url(r'^echo$', echo),

    # oauth entrypoints
    url(r'^oauth/request_token$', 'piston.authentication.oauth_request_token'),
    url(r'^oauth/authorize$', 'piston.authentication.oauth_user_auth'),
    url(r'^oauth/access_token$', 'piston.authentication.oauth_access_token'),

    url(r'^list_fields$', list_fields),
    url(r'^list_fields/(?P<id>.+)$', list_fields),
    
    url(r'^popo$', popo),
)


