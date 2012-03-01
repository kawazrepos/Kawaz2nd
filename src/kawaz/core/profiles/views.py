#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
View models of profile application


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
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic import DetailView

from qwert.http import Http403
from object_permission.decorators import permission_required

from kawaz.core import get_children_pgroup

from models import Profile
from forms import ProfileForm
from forms import ServiceFormSet


class ProfileListView(ListView):
    """Profile list view"""
    def get_queryset(self):
        return Profile.objects.published(self.request)

@permission_required('profiles.view_profile')
class ProfileDetailView(DetailView):
    model = Profile
    slug_field = 'user__username'
    
from django.views.generic.edit import ProcessFormView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin

@permission_required('profiles.change_profile')
class ProfileUpdateView(
        SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    """Profile update view

    Authenticated user only can update own profile
    """
    template_name_suffix = '_form'
    form_class = ProfileForm
    formset_class = ServiceFormSet
    
    def get_object(self, queryset=None):
        children = get_children_pgroup()
        if children.is_belong(self.request.user):
            return self.request.user.get_profile()
        return None
        
    def get_formset_class(self):
        return self.formset_class
    def get_formset(self, formset_class):
        return formset_class(**self.get_form_kwargs())

    def form_valid(self, form, formset):
        formset.save()
        return super(ProfileUpdateView, self).form_valid(form)
    def form_invalid(self, form, formset):
        context = self.get_context_data(
                form=form, formset=formset)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.request = request
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        context = self.get_context_data(
            form=form, formset=formset)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)
