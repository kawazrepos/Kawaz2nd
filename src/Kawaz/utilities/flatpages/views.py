# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/09
#
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.decorators import permission_required
from libwaz.views.generic import list_detail
from libwaz.views.generic import create_update
from django.core.urlresolvers import reverse

import forms

#
# list_detail
#-----------------------------------------------------------
@permission_required('flatpages.view_flatpage')
def flatpage_list(request):
    kwargs = {
        'queryset': FlatPage.objects.all(),
    }
    return list_detail.object_list(request, **kwargs)

#
# create_update
#-----------------------------------------------------------
@permission_required('flatpages.add_flatpage')
def create_flatpage(request):
    kwargs = {
        'form_class': forms.FlatPageForm,
        'initial_with_get': True,
    }
    return create_update.create_object(request, **kwargs)
@permission_required('flatpages.change_flatpage')
def update_flatpage(request, object_id):
    kwargs = {
        'form_class': forms.FlatPageForm,
    }
    return create_update.update_object(request, object_id=object_id, **kwargs)
@permission_required('flatpages.delete_flatpage')
def delete_flatpage(request, object_id):
    kwargs = {
        'model': FlatPage,
        'post_delete_redirect': reverse('flatpages-flatpage-list'),
    }
    return create_update.delete_object(request, object_id=object_id, **kwargs)
