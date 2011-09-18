#-*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User

from libwaz.views.generic import list_detail
from libwaz.views.generic import create_update
from libwaz.contrib.object_permission.decorators import permission_required

from models import Project, Category
from forms import ProjectForm, ProjectUpdateForm
from filtersets import ProjectFilterSet

def withauthor(fn):
    def inner(request, *args, **kwargs):
        if 'author' in kwargs:
            if not isinstance(kwargs['author'], User):
                author = get_object_or_404(User, username=kwargs['author'])
                kwargs['author'] = author
        else:
            kwargs['author'] = None
        return fn(request, *args, **kwargs)
    return inner
def withcategory(fn):
    def inner(request, *args, **kwargs):
        if 'category' in kwargs:
            if not isinstance(kwargs['category'], Category):
                category = get_object_or_404(Category, label=kwargs['category'])
                kwargs['category'] = category
        else:
            kwargs['category'] = None
        return fn(request, *args, **kwargs)
    return inner
#
# list_detail
#---------------------------------------------------------------------------------------
@withcategory
@withauthor
def project_filter(request, author=None, category=None):
    qs = Project.objects.published(request)
    if author:
        qs = qs.filter(author=author)
    if category:
        qs = qs.filter(category=category)
    kwargs = {
        'queryset': qs,
        'filter_class': ProjectFilterSet,
        'extra_context': {
            'author': author,
            'category': category,
        }
    }
    return list_detail.object_filter(request, **kwargs)

@permission_required('projects.view_project', Project)
def project_detail(request, slug):
    kwargs = {
        'queryset': Project.objects.published(request),
    }
    return list_detail.object_detail(request, slug=slug, **kwargs)

#
# create_update
#----------------------------------------------------------------------------------------
@permission_required('projects.add_project')
def create_project(request, *args, **kwargs):
    kwargs = {
        'form_class': ProjectForm,
    }
    return create_update.create_object(request, **kwargs)

@permission_required('projects.change_project', Project)
def update_project(request, object_id):
    kwargs = {
        'form_class': ProjectUpdateForm,
    }
    return create_update.update_object(request, object_id=object_id, **kwargs)

@permission_required('projects.delete_project', Project)
def delete_project(request, object_id):
    kwargs = {
        'model': Project,
        'post_delete_redirect': reverse('projects-project-list'),
    }
    return create_update.delete_object(request, object_id=object_id, **kwargs)

#
# API
#------------------------------------------------------------------------------------------
@permission_required('projects.join_project', Project)
def join_project(request, object_id):
    obj = get_object_or_404(Project, pk=object_id)
    # プロジェクトに参加させる
    obj.join(request.user)
    messages.success(request, u"プロジェクト「%s」に参加しました" % obj.title, fail_silently=True)
    return redirect(obj)

@permission_required('projects.join_project', Project)
def quit_project(request, object_id, user=None):
    obj = get_object_or_404(Project, pk=object_id)
    if user:
        user = get_object_or_404(User, username=user)
        if not request.user.has_perm('projects.kick_project', obj):
            messages.error(request, u"ユーザーをキックできるのは管理者のみです", fail_silently=True)
            return redirect(obj)
        msg = u"%sをプロジェクト「%s」からキックしました" % (user.get_profile().nickname, obj.title)
    else:
        user = request.user
        msg = u"プロジェクト「%s」への参加をやめました" % obj.title
    if user == obj.author:
        messages.error(request, u"プロジェクト管理者はプロジェクトから離脱できません", fail_silently=True)
        return redirect(obj)
    # プロジェクト参加をやめる
    obj.quit(user)
    messages.success(request, msg, fail_silently=True)
    return redirect(obj)
