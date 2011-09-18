# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/11
#
from piston.handler import BaseHandler

from ..models import Project

class ProjectHandler(BaseHandler):
    allowed_method = ('GET',)
    model = Project
    fields = (
        'id', 'slug', 'title', 'get_absolute_url',
        'pub_state', 'status', 'permission',
        'body', 'icon', 'updated_at', 'publish_at',
        ('author', ('id', 'username', ('profile', (
            'nickname',
        )))),
        ('members', ('id', 'username', ('profile', (
            'nickname',
        )))),
    )
    
    def read(self, request, object_id=None):
        qs = Project.objects.published(request)
        
        if object_id:
            return qs.get(pk=object_id)
        return qs.all()