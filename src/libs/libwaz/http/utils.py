# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/26
#
from django.http.utils import *

from django.db.models.base import ModelBase
from django.utils import simplejson
from django.utils.encoding import force_unicode

class LazyJSONEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        try:
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        try:
            isinstance(obj.__class__, ModelBase)
        except Exception:
            pass
        else:
            return force_unicode(obj)
        return super(LazyJSONEncoder, self).default(obj)

def serialize_to_json(obj, *args, **kwargs):
    kwargs['ensure_ascii'] = kwargs.get('ensure_ascii', False)
    kwargs['cls'] = kwargs.get('cls', LazyJSONEncoder)
    return simplejson.dumps(obj, *args, **kwargs)