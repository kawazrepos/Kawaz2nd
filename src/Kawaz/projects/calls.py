# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from libwaz.contrib.calls import site
from libwaz.contrib.calls.backends.idcalls import IdCallsBackend

from models import Project

class ProjectCallsBackend(IdCallsBackend):
    def autodiscover(self, instance, **kwargs):
        if instance.pub_state == 'draft':
            return
        super(ProjectCallsBackend, self).autodiscover(instance, **kwargs)
site.register(Project, ProjectCallsBackend)