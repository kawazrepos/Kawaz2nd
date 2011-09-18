# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/01
#
from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc, validate

from ..models import Tweet
from ..forms import TweetAjaxForm

class TweetHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'DELETE')
    fields = (
        'get_absolute_url',
        'body', 'source', 'created_at', 
        ('author', ('username', )),
        ('reply', ('body', 'source', 'created_at', ('author', 'username', ))),
    )
    model = Tweet
    anonymous = 'AnonymousTweetHandler'

    def read(self, request, object_id=None):
        base = Tweet.objects
        
        if object_id:
            return base.filter(pk=object_id)
        else:
            return base.all()
    
    @validate(TweetAjaxForm)
    def create(self, request):
        attrs = request.form.cleaned_data
        instance = self.model.objects.create(
            author=request.user,
            **attrs
        )
        
        return instance
    
    def delete(self, request, object_id):
        obj = self.model.objects.get(pk=object_id)
        obj.delete()
        
        return rc.DELETE
class AnonymousTweetHandler(TweetHandler, AnonymousBaseHandler):
    model = Tweet