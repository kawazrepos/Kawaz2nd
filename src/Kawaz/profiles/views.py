# -*- coding: utf-8 -*-
#
# Created:    2010/09/24
# Author:         alisue
#
from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login
from django.views.decorators.http import require_POST
from django.views.generic.simple import direct_to_template

from libwaz.http import JsonResponse, Http403
from libwaz.views.generic import list_detail
from libwaz.contrib.object_permission.utils import generic_permission_check

from models import Profile
from filtersets import ProfileFilterSet
from forms import get_service_formset, ProfileForm, ServiceForm


def permission_required(perm, model=None):
    def wrapper(fn):
        def inner(request, *args, **kwargs):
            if model:
                queryset = model.objects.all()
            else:
                queryset = None
            kwargs['slug_field'] = 'user__username'
            if not generic_permission_check(queryset, perm, request, *args, **kwargs):
                if request.user.is_authenticated():
                    raise Http403
                else:
                    return redirect_to_login(request.path)
            return fn(request, *args, **kwargs)
        return inner
    return wrapper
#
# list_detail
#-------------------------------------------------------------------------------
def profile_filter(request):
    kwargs = {
        'queryset': Profile.objects.published(request),
        'filter_class': ProfileFilterSet,
    }
    return list_detail.object_filter(request, **kwargs)
@permission_required('profiles.view_profile', Profile)
def profile_detail(request, slug, slug_field):
    kwargs = {
        'queryset': Profile.objects.published(request),
    }
    return list_detail.object_detail(request, slug=slug, slug_field=slug_field, **kwargs)

#
# API
#--------------------------------------------------------------------------------
@require_POST
def update_mood_json(request):
    if not request.user.is_authenticated():
        return JsonResponse({'state': 'Failed'})
    profile = request.user.get_profile()
    # 改行コードは入らないようにJSでやっているはずだが一応<br>は消しておく
    profile.mood = request.POST.get('mood', '').replace('<br>', "").strip()
    profile.save()
    return JsonResponse({'state': 'OK'})


def update_profile(request):
    ServiceFormset = get_service_formset(ServiceForm, extra=1, can_delete=True)
    if request.user.is_authenticated():
        profile = request.user.get_profile()
    else:
        raise Http403
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        formset = ServiceFormset(request.POST, request.FILES, instance=profile)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect(profile)
    else:
        form = ProfileForm(instance=profile)
        formset = ServiceFormset(instance=profile)
    return direct_to_template(request,
        template="profiles/profile_form.html",
        extra_context={'object':profile, 'form':form, 'formset':formset}
    )
