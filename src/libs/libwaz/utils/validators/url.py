# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/11
#
from urlparse import urlparse
from django.core.urlresolvers import resolve, Resolver404

def url_exists(value):
    try: resolve(urlparse('/' + value + '/')[2])
    except Resolver404:
        return False
    return True