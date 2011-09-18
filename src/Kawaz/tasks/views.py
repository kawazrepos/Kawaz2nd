# -*- coding:utf-8 -*-
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from libwaz.http import Http403
from libwaz.views.generic import list_detail
from libwaz.views.generic import create_update
from libwaz.contrib.object_permission.decorators import permission_required

from ..projects.models import Project

from models import Task
from forms import TaskForm
from filtersets import TaskFilterSet

def withproject(fn):
    def inner(request, *args, **kwargs):
        if 'project' in kwargs:
            project = kwargs['project']
            if isinstance(project, basestring):
                project = get_object_or_404(Project, slug=project)
            kwargs['project'] = project
        return fn(request, *args, **kwargs)
    return inner
#
# list_detail
#--------------------------------------------------------------------------------------------
@withproject
def task_filter(request, project=None):
    if project:
        qs = Task.objects.published(request).filter(project=project)
    else:
        if not request.user.is_authenticated():
            # ログインしていないユーザーは自分のタスク一覧を見れない
            raise Http403
        qs = Task.objects.relative(request, request.user)
    kwargs= {
        'queryset': qs,
        'filter_class': TaskFilterSet,
        'extra_context': {
            'project': project,
        },
    }
    return list_detail.object_filter(request, **kwargs)
@permission_required('tasks.view_task', Task)
def task_detail(request, object_id):
    kwargs = {
        'queryset': Task.objects.published(request),
    }
    return list_detail.object_detail(request, object_id=object_id, **kwargs)

#
# create_update
#---------------------------------------------------------------------------------------------
@withproject
@permission_required('tasks.add_task')
def create_task(request, project=None):
    kwargs = {
        'form_class': TaskForm,
        'extra_context': {
            'project': project
        },
    }
    if project:
        if not request.user.has_perm('projects.add_task_project', project):
            raise Http403
        kwargs['initial'] = {
            'project': project.pk
        }
    return create_update.create_object(request, **kwargs)
@permission_required('tasks.change_task', Task)
def update_task(request, object_id):
    kwargs = {
        'form_class': TaskForm,
    }
    return create_update.update_object(request, object_id=object_id, **kwargs)
@permission_required('tasks.delete_task', Task)
def delete_task(request, object_id):
    kwargs = {
        'model': Task,
        'post_delete_redirect': reverse('tasks-task-list'),
    }
    return create_update.delete_object(request, object_id=object_id, **kwargs)

#
# API
#------------------------------------------------------------------------------------------------
@permission_required('tasks.status_task', Task)
def update_task_status(request, object_id, status):
    obj = get_object_or_404(Task, pk=object_id)
    if status == 'join':
        # 担当者になる
        obj.join(request.user)
        if obj.owners.count() == 1:
            obj.status = 'accepted'
            obj.save()
        return redirect(obj)
    elif status == 'canceled':
        # 担当者から外れる
        obj.quit(request.user)
        if obj.owners.count() == 0:
            obj.status = 'canceled'
            obj.save()
        return redirect(obj)
    elif not status in dict(Task.STATUSES).keys():
        # TODO: エラーをJson形式で返す
        raise ValidationError(u"Invalid status")
    obj.status = status
    obj.save(request=request, action=status)
    return redirect(obj)