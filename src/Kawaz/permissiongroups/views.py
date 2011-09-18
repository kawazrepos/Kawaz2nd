# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/08
#
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse

from libwaz.http import Http403
from libwaz.views.generic import list_detail
from libwaz.views.generic import create_update

import forms
import models

#
# list_detail
#------------------------------------------------------------------
@permission_required('permissiongroups.view_permissiongroup')
def permissiongroup_list(request):
    kwargs = {
        'queryset': models.PermissionGroup.objects.all(),
    }
    return list_detail.object_list(request, **kwargs)
@permission_required('permissiongroups.view_permissiongroup')
def permissiongroup_detail(request, object_id):
    obj = get_object_or_404(models.PermissionGroup, pk=object_id)
    kwargs = {
        'queryset': models.PermissionGroup.objects.all(),
        'extra_context': {
            'form': forms.PartialPermissionGroupForm(instance=obj),
        }
    }
    return list_detail.object_detail(request, object_id=object_id, **kwargs)

#
# create_update
#-------------------------------------------------------------------
@permission_required('permissiongroups.add_permissiongroup')
def create_permissiongroup(request):
    kwargs = {
        'form_class': forms.PermissionGroupForm,
    }
    return create_update.create_object(request, **kwargs)
@permission_required('permissiongroups.change_permissiongroup')
def update_permissiongroup(request, object_id):
    kwargs = {
        'form_class': forms.PermissionGroupForm,
    }
    return create_update.update_object(request, object_id=object_id, **kwargs)
@permission_required('permissiongroups.delete_permissiongroup')
def delete_permissiongroup(request, object_id):
    kwargs = {
        'model': models.PermissionGroup,
        'post_delete_redirect': reverse('permissiongroups-permissiongroup-list'),
    }
    return create_update.delete_object(request, object_id=object_id, **kwargs)

#
# API
#-------------------------------------------------------------------
def promote(request):
    if not request.user.is_promotable:
        raise Http403
    next = request.GET.get('next', '/')
    request.user.is_superuser = True
    request.user.save()
    return redirect(next)

def demote(request):
    if not request.user.is_promotable:
        raise Http403
    next = request.GET.get('next', '/')
    request.user.is_superuser = False
    request.user.save()
    return redirect(next)