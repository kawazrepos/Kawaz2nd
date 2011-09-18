# -*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import simple
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse

from libwaz.db.models import Model
from libwaz.http import Http403, Http404
from libwaz.views.generic import list_detail
from libwaz.views.generic import create_update
from libwaz.contrib.object_permission.utils import generic_permission_check

from ..projects.models import Project
from models import Entry
from forms import EntryForm
from filtersets import EntryFilterSet

def withproject(fn):
    def inner(request, *args, **kwargs):
        if 'project' in kwargs:
            project = kwargs['project']
            if not isinstance(project, Model):
                project = get_object_or_404(Project, slug=project)
            kwargs['project'] = project
        return fn(request, *args, **kwargs)
    return inner
def permission_required(perm, model=None):
    def wrapper(fn):
        def inner(request, *args, **kwargs):
            if not isinstance(kwargs['project'], Project):
                project = get_object_or_404(Project, slug=kwargs['project'])
            else:
                project = kwargs['project']
            if model:
                queryset = model.objects.filter(project=project)
            else:
                queryset = None
            if model and not 'slug_field' in kwargs:
                kwargs['slug_field'] = 'title'
            if model and not 'slug' in kwargs:
                kwargs['slug'] = 'index'
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
#----------------------------------------------------------------------
@withproject
def entry_filter(request, project):
    kwargs = {
        'queryset': Entry.objects.published(request).filter(project=project),
        'filter_class': EntryFilterSet,
        'extra_context': {
            'project': project,
        }
    }
    return list_detail.object_filter(request, **kwargs)
@withproject
@permission_required('wikis.view_entry', Entry)
def entry_detail(request, project, slug='index', slug_field='title'):
    try:
        obj = Entry.objects.get(project=project, **{slug_field: slug})
        template = r'wikis/entry_detail.html'
        extra_context = {
            'object': obj,
            'project': project,
        }
    except Entry.DoesNotExist:
        if not request.user.has_perm('projects.add_wiki_project', project):
            raise Http404
        template = r'wikis/entry_confirm_create.html'
        extra_context = {
            'project': project,
            'title': slug,
        }
    return simple.direct_to_template(request, template, extra_context)

#
# create_update
#-----------------------------------------------------------------------
@withproject
@permission_required('wikis.add_entry')
def create_entry(request, project):
    if not request.user.has_perm('projects.add_wiki_project', project):
        raise Http403
    kwargs = {
        'form_class': EntryForm,
        'initial': {
            'project': project.pk,
        },
        'initial_with_get': True,
        'extra_context': {
            'project': project,
        }
    }
    return create_update.create_object(request, **kwargs)
@withproject
@permission_required('wikis.change_entry', Entry)
def update_entry(request, project, slug, slug_field='title'):
    obj = get_object_or_404(Entry, project=project, title=slug)
    kwargs = {
        'form_class': EntryForm,
        'extra_context': {
            'project': project,
        }
    }
    return create_update.update_object(request, object_id=obj.pk, **kwargs)
@withproject
@permission_required('wikis.delete_entry', Entry)
def delete_entry(request, project, slug, slug_field='title'):
    obj = get_object_or_404(Entry, project=project, title=slug)
    kwargs = {
        'model': Entry,
        'post_delete_redirect': obj.get_absolute_url(),
        'extra_context': {
            'project': project,
        }
    }
    return create_update.delete_object(request, object_id=obj.pk, **kwargs)