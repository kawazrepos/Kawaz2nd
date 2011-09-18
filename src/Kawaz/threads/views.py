# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from libwaz.http import Http403
from libwaz.views.generic import list_detail
from libwaz.views.generic import create_update
from libwaz.contrib.object_permission.decorators import permission_required

from ..projects.models import Project
from models import Thread
from forms import ThreadForm
from filtersets import ThreadFilterSet

#
# list_detail
#-------------------------------------------------------------------------------------
def thread_filter(request, project=None):
    qs = Thread.objects.published(request)
    if project:
        project = get_object_or_404(Project, slug=project)
        qs = qs.filter(project=project)
    kwargs = {
        'queryset': qs,
        'filter_class': ThreadFilterSet,
        'extra_context': {
            'project': project,
        },
    }
    return list_detail.object_filter(request, **kwargs)
@permission_required('threads.view_thread', Thread)
def thread_detail(request, object_id, param=None):
#    def tryInt(x):
#        try:
#            return int(x)-1
#        except:
#            return None
    obj = get_object_or_404(Thread, pk=object_id)
    # Notice:
    #   下記コメントアウトをとれば2ch風のURLマッピングで表示スレッド数を制限可能だが
    #   レスNoをforloop.countで出しているため表示スレッド数をviewで制限すると
    #   レスNoがずれる。したがって廃止した。
#    start, end = None, None
#    if param:
#        bits = param.split('-')
#        if len(bits) == 2:
#            start = tryInt(bits[0])
#            end = tryInt(bits[1])
#        elif len(bits) == 1:
#            start = tryInt(bits[0])
#            end = None
#    response_list = obj.response()[start:end]
    response_list = obj.response()
    kwargs = {
        'queryset': Thread.objects.published(request),
        'extra_context': {
            'response_list': response_list,
        }
    }
    return list_detail.object_detail(request, object_id=object_id, **kwargs)

#
# create_update
#-------------------------------------------------------------------------------------
@permission_required('threads.add_thread')
def create_thread(request, project=None):
    if project:
        project = get_object_or_404(Project, slug=project)
        if not request.user.has_perm('projects.add_thread_project', project):
            raise Http403
    kwargs = {
        'form_class': ThreadForm,
        'extra_context': {
            'project': project,
        },
    }
    if project:
        kwargs['initial'] = {'project': project.pk}
    return create_update.create_object(request, **kwargs)
@permission_required('threads.change_thread', Thread)
def update_thread(request, object_id):
    kwargs = {
        'form_class': ThreadForm,
    }
    return create_update.update_object(request, object_id=object_id, **kwargs)
@permission_required('threads.delete_thread', Thread)
def delete_thread(request, object_id):
    kwargs = {
        'model': Thread,
        'post_delete_redirect': reverse('threads-thread-list'),
    }
    return create_update.delete_object(request, object_id=object_id, **kwargs)
