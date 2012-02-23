#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Views of registration-request


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
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from registration.views import register
from registration.backends import get_backend

from forms import ActivationForm

def activate(request, activation_key, backend, success_url=None, form_class=ActivationForm,
             template_name='registration/activation_form.html',
             extra_context=None):
    backend = get_backend(backend)

    if not backend.is_valid_activation_key(activation_key):
        raise Http404()

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            password = form.cleaned_data['password1']
            activated = backend.activate(request, activation_key, password=password)
            if success_url is None:
                to, args, kwargs = backend.post_activation_redirect(request, activated)
                return redirect(to, *args, **kwargs)
            else:
                return redirect(success_url)
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)
