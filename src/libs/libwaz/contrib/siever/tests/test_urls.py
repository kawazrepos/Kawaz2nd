from django.conf.urls.defaults import *

from models import Book

from ..views import object_filter

urlpatterns = patterns('',
    (r'^books/$', object_filter, {'model': Book}),
)
