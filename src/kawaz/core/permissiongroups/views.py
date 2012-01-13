#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
PermissionGroup views


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
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse

from kawaz.utils.decorators import permission_required

from models import PermissionGroup
from forms import PermissionGroupForm
from forms import PartialPermissionGroupForm

class PermissionGroupMixin(object):
    queryset = PermissionGroup.objects.all()

class PermissionGroupFormMixin(object):
    form_class = PermissionGroupForm

@permission_required('permissiongroups.view_permissiongroup')
class PermissionGroupListView(ListView, PermissionGroupMixin):
    pass

@permission_required('permissiongroups.view_permissiongroup')
class PermissionGroupDetailView(DetailView, PermissionGroupMixin):
    def get_context_data(self, **kwargs):
        context_data = super(PermissionGroupDetailView, self).get_context_data(**kwargs)
        context_data['form'] = PartialPermissionGroupForm(instance=self.get_object())
        return context_data

@permission_required('permissiongroups.add_permissiongroup')
class PermissionGroupCreateView(CreateView, PermissionGroupFormMixin):
    pass

@permission_required('permissiongroups.change_permissiongroup')
class PermissionGroupUpdateView(UpdateView, PermissionGroupFormMixin):
    pass

@permission_required('permissiongroups.delete_permissiongroup')
class PermissionGroupDeleteView(DeleteView, PermissionGroupFormMixin):
    def get_success_url(self):
        return reverse('permissiongroups-permissiongroup-list')
