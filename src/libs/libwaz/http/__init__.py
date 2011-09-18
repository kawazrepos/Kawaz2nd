# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/26
#
from django.http import *
from utils import serialize_to_json

class Http403(Exception):
    pass

class JsonResponse(HttpResponse):
    """A HTTP response, with Json content and dictionary-accessed headers."""
    
    def __init__(self, content='', json_opts={}, mimetype="text/html", *args, **kwargs):
        if content:
            content = serialize_to_json(content, **json_opts)
        else:
            content = serialize_to_json([], **json_opts)
        super(JsonResponse, self).__init__(content, *args, mimetype=mimetype, **kwargs)