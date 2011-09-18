# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/26
#
from django.middleware.http import *
from django.http import HttpResponseForbidden
from django.template import RequestContext, loader

from ..http import Http403

class Http403Middleware(object):
    def process_exception(self, request, exception):
        if not isinstance(exception, Http403):
            # Return None so django doesn't re-raise the exception
            return None
        
        c = RequestContext(request, {
            'message': exception
        })
        return HttpResponseForbidden(loader.get_template('403.html').render(c))