# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/11
#
from django.conf.urls.defaults import *
from piston.resource import Resource
from handlers import ProjectHandler

project_handler = Resource(ProjectHandler)

urlpatterns = patterns('',
   url(r'^project/(?P<object_id>\d+)/$',     project_handler,    name="projects-project-api"),
   url(r'^projects/$',                       project_handler,    name="projects-project-api"),
)
