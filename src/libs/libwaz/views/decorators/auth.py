# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
from django.shortcuts import redirect
from libwaz.http import Http403

__all__ = ['login_required', 'staff_required', 'superuser_required']

def login_required(fn):
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('auth_login')
        return fn(request, *args, **kwargs)
    return inner

def staff_required(fn):
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('auth_login')
        if not request.user.is_staff and not request.user.is_superuser:
            raise Http403
        return fn(request, *args, **kwargs)
    return inner

def superuser_required(fn):
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('auth_login')
        if not request.user.is_superuser:
            raise Http403
        return fn(request, *args, **kwargs)
    return inner