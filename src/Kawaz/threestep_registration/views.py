# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/08
#
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext_lazy as _

from backends import get_backend
from models import RegistrationProfile
from forms import RegistrationHandleForm, CSVRegistrationForm

def activate(request, backend,
             template_name='registration/activate.html',
             success_url=None, extra_context=None, **kwargs):
    backend = get_backend(backend)
    account = backend.activate(request, **kwargs)

    if account:
        if success_url is None:
            to, args, kwargs = backend.post_activation_redirect(request, account)
            return redirect(to, *args, **kwargs)
        else:
            return redirect(success_url)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              kwargs,
                              context_instance=context)


def register(request, backend, success_url=None, form_class=None,
             disallowed_url='registration_disallowed',
             template_name='registration/registration_form.html',
             extra_context=None):
    backend = get_backend(backend)
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)
    if form_class is None:
        form_class = backend.get_form_class(request)

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = backend.register(request, **form.cleaned_data)
            if success_url is None:
                to, args, kwargs = backend.post_registration_redirect(request, new_user)
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

@permission_required('threestep_registration.view_registrationprofile')
@csrf_protect
def list(request, backend, template_name=r'registration/list.html', extra_context=None):
    if extra_context is None:
        extra_context = {}
    if request.method == 'POST':
        form = RegistrationHandleForm(request.POST)
        if form.is_valid():
            backend = get_backend(backend)
            action = form.cleaned_data['action']
            registration_profiles = form.cleaned_data['registration_profiles']
            if action == 'approve' and request.user.has_perm('threestep_registration.approve_registrationprofile'):
                success_users = backend.approve(request, registration_profiles)
            elif action == 'reject' and request.user.has_perm('threestep_registration.reject_registrationprofile'):
                success_users = backend.reject(request, registration_profiles)
            else:
                return HttpResponseForbidden()
            users = [registration_profile.user for registration_profile in registration_profiles]
            success_user_ids = [user.pk for user in success_users]
            failed_users = [user for user in users if not user.pk in success_user_ids]
            verbose_action = dict(RegistrationHandleForm.ACTIONS)[action]
            message = []
            for user in success_users:
                message.append(_('You have %(action)s "%(user)s"') % {'action': verbose_action, 'user': user.username})
            messages.success(request, "\n".join(message), fail_silently=True)
            message = []
            for user in failed_users:
                message.append(_('Failed to %(action)s "%(user)s"') % {'action': verbose_action, 'user': user.username})
            messages.error(request, "\n".join(message), fail_silently=True)
    else:
        form = RegistrationHandleForm()
    extra_context['form'] = form
    extra_context['registered_profiles'] = RegistrationProfile.objects.filter(status='waiting')
    extra_context['approved_profiles'] = RegistrationProfile.objects.filter(status='approved', user__is_active=False)
    return direct_to_template(request, template_name, extra_context=extra_context)

def withdraw(request):
    if request.method == 'POST':
        request.user.is_active = False
        request.user.save()
        from signals import user_withdrawed
        user_withdrawed.send(sender=withdraw, user=request.user, request=request)
        logout(request)
        return direct_to_template(request, template='registration/withdraw_done.html')
    else:
        return direct_to_template(request, template='registration/withdraw_confirm.html')

@permission_required('threestep_registration.view_registrationprofile')
@csrf_protect
def csv_registration(request, backend, template_name=r'registration/csv_registration_form.html', extra_context=None):
    from utils import register_from_csv
    if extra_context is None:
        extra_context = {}
    if request.method == 'POST':
        form = CSVRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            success_users = register_from_csv(request, backend, form.cleaned_data['csv_file'])
            messages.success(request, _('%d users successfully appended from CSV file.') % len(success_users), fail_silently=True)
    else:
        form = CSVRegistrationForm()
    extra_context['form'] = form
    return direct_to_template(request, template_name, extra_context=extra_context)