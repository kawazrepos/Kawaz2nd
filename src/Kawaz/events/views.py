# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from libwaz.http import Http403
from libwaz.views.generic import list_detail
from libwaz.views.generic import date_based
from libwaz.views.generic import create_update
from libwaz.contrib.object_permission.decorators import permission_required

from models import Event
from forms import EventForm
from filtersets import EventFilterSet

#
# list_detail
#-------------------------------------------------------------------------
def event_filter(request):
    kwargs = {
        'queryset': Event.objects.active(request),
        'filter_class': EventFilterSet,
    }
    return list_detail.object_filter(request, **kwargs)

@permission_required('events.view_event', Event)
def event_detail(request, object_id):
    kwargs = {
        'queryset': Event.objects.published(request),
    }
    return list_detail.object_detail(request, object_id=object_id, **kwargs)

#
# create_update
#--------------------------------------------------------------------------
@permission_required('events.add_event')
def create_event(request):
    kwargs = {
        'form_class': EventForm
    }
    return create_update.create_object(request, **kwargs)
@permission_required('events.change_event', Event)
def update_event(request, object_id):
    kwargs = {
        'form_class': EventForm
    }
    return create_update.update_object(request, object_id=object_id, **kwargs)
@permission_required('events.delete_event', Event)
def delete_event(request, object_id):
    kwargs = {
        'model': Event,
        'post_delete_redirect': reverse('events-event-list')
    }
    return create_update.delete_object(request, object_id=object_id, **kwargs)

#
# date_based
#---------------------------------------------------------------------------
def event_archive_year(request, year):
    kwargs = {
        'queryset': Event.objects.published(request),
        'date_field': 'period_start',
        'allow_empty': True,
        'allow_future': True,
    }
    return date_based.archive_year(request, year=year, **kwargs)
def event_archive_month(request, year, month):
    kwargs = {
        'queryset': Event.objects.published(request),
        'date_field': 'period_start',
        'month_format': '%m',
        'allow_empty': True,
        'allow_future': True,
    }
    return date_based.archive_month(request, year=year, month=month, **kwargs)
def event_archive_day(request, year, month, day):
    kwargs = {
        'queryset': Event.objects.published(request),
        'date_field': 'period_start',
        'month_format': '%m',
        'allow_empty': True,
        'allow_future': True,
    }
    return date_based.archive_day(request, year=year, month=month, day=day, **kwargs)

#
# API
#-------------------------------------------------------------------------------
@permission_required('events.join_event', Event)
def join_event(request, object_id):
    obj = get_object_or_404(Event, pk=object_id)
    # イベントに参加させる
    obj.join(request.user)
    messages.success(request, u"イベント「%s」に参加しました" % obj.title, fail_silently=True)
    return redirect(obj)

@permission_required('events.join_event', Event)
def quit_event(request, object_id, user=None):
    obj = get_object_or_404(Event, pk=object_id)
    if user:
        user = get_object_or_404(User, username=user)
        if not request.user.has_perm('events.kick_event', obj):
            messages.error(request, u"ユーザーをキックできるのは管理者のみです", fail_silently=True)
            return redirect(obj)
        msg = u"%sをイベント「%s」からキックしました" % (user.get_profile().nickname, obj.title)
    else:
        user = request.user
        msg = u"イベント「%s」への参加をやめました" % obj.title
    if user == obj.author:
        messages.error(request, u"イベント企画者は参加を取りやめることができません", fail_silently=True)
        return redirect(obj)
    # イベント参加をやめる
    obj.quit(user)
    messages.success(request, msg, fail_silently=True)
    return redirect(obj)
