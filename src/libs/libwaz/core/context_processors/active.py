# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
# from snippets: http://djangosnippets.org/snippets/2143/
#
from django.core.urlresolvers import reverse, resolve

def get_view(name, *args, **kwargs):
    return resolve(reverse(name, args=args, kwargs=kwargs))[0]

class ActiveMenu(object):
    """ mapping urls to selected menu items """

    url_map = {
        get_view('admin:customer_customer_add'):        'customer',
        get_view('admin:customer_customer_change', 0):  'customer',
        get_view('admin:customer_customer_changelist'): 'customer',

        get_view('admin:product_product_add'):          'product',
        get_view('admin:product_product_change', 0):    'product',
        get_view('admin:product_product_changelist'):   'product',
    }

    def __init__(self, request):
        self.active = self.url_map.get(resolve(request.path)[0])

    def __getattr__(self, name):
        return self.active == name

def menu(request):
    """ enable this context processor in settings.py """
    return { 'menu': ActiveMenu(request) }
