# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
# from snippets: http://djangosnippets.org/snippets/2195/
#
from django.http import HttpResponse
from django.shortcuts import render_to_response as _render_to_response
from django.template import RequestContext

__all__ = ['render_to_response']
def render_to_response(func):
    def inner(request, *args, **kwargs):
        result = func(request, *args, **kwargs)
        if isinstance(result, HttpResponse):
            return result
        if len(result) == 2:
            template, dictionary = result
            context_instance=RequestContext(request)
        else:
            template, dictionary, context_instance = result
        return _render_to_response(template, dictionary, context_instance)
    return inner