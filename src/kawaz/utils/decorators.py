#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Decorator utils and shortuct decorator for classbased generic view

AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
from django.utils.decorators import method_decorator as _method_decorator


def method_decorator(decorator):
    """Converts a function decorator into a method decorator"""
    if decorator.__name__.startswith('method_decorator'):
        # do nothing
        return decorator
    return _method_decorator(decorator)
    

def view_class_decorator(decorator):
    """Converts a function decorator into a Generic View Class decorator"""
    def _decorator(cls):
        dispatch = getattr(cls, 'dispatch')
        func = method_decorator(decorator)
        dispatch = func(dispatch)
        setattr(cls, 'dispatch', dispatch)
        return cls
    return _decorator


from django.contrib.auth.decorators import login_required as _login_required
from django.contrib.auth.decorators import permission_required as _permission_required


def login_required(*args, **kwargs):
    """
    Decorator for classbased views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    return view_class_decorator(_login_required(*args, **kwargs))


def permission_required(*args, **kwargs):
    """
    Decorator for classbased views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if neccesary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    return view_class_decorator(_permission_required(*args, **kwargs))
