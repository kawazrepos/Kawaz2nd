# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/25
#
#
# Supports:
#    + method = 'json'
#    + ModelWithRequest, ModelFormWithRequest
#
from libwaz.views.generic.json import create_update

def create_object(request, *args, **kwargs):
    if not 'method' in kwargs:
        kwargs['method'] = 'html'
    return create_update.create_object(request, *args, **kwargs) 

def update_object(request, *args, **kwargs):
    if not 'method' in kwargs:
        kwargs['method'] = 'html'
    return create_update.update_object(request, *args, **kwargs) 

def delete_object(request, *args, **kwargs):
    if not 'method' in kwargs:
        kwargs['method'] = 'html'
    return create_update.delete_object(request, *args, **kwargs) 