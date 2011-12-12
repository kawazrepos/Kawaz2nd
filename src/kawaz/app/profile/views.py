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
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic import DetailView

from qwert.http import Http403
from django_filters.generic.classbase import FilterView

from models import Profile
from filtersets import ProfileFilterSet
from forms import ProfileForm
from forms import ServiceFormSet

def permission_required(perm, model=None):
    """permission required decorator"""
    from django.contrib.auth.views import redirect_to_login
    from qwert.http import Http403
    from object_permission.utils import generic_permission_check
    def wrapper(fn):
        def inner(request, *args, **kwargs):
            queryset = None
            if model:
                queryset = model.objects.all()
            kwargs['slug_field'] = 'user__username'
            if not generic_permission_check(
                    queryset, perm, request, *args, **kwargs):
                if request.user.is_authenticated():
                    raise Http403
                else:
                    return redirect_to_login(request.path)
            return fn(request, *args, **kwargs)
        return inner
    return wrapper


class ProfileFilterView(FilterView):
    """Profile filter view"""
    filter_class = ProfileFilterSet

    def get_queryset(self):
        return Profile.objects.published(self.request)

class ProfileListView(ListView):
    """Profile list view"""
    def get_queryset(self):
        return Profile.objects.published(self.request)

class ProfileDetailView(DetailView):
    model = Profile
    slug_field = 'user__username'
    
    @method_decorator(permission_required('profile.view_profile', Profile))
    def dispatch(self, *args, **kwargs):
        return super(ProfileDetailView, self).dispatch(*args, **kwargs)

from django.views.generic.edit import ProcessFormView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin

class ProfileUpdateView(
        SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    """Profile update view

    Authenticated user only can update own profile
    """
    template_name_suffix = '_form'
    form_class = ProfileForm
    formset_class = ServiceFormSet
    
    def get_object(self):
        if not self.request.user.is_authenticated():
            raise Http403('You are not logged in')
        return self.request.user.get_profile()
        
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
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        context = self.get_context_data(
            form=form, formset=formset)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)
