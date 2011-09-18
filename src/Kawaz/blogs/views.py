# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse

from libwaz.http import Http403
from libwaz.views.generic import list_detail
from libwaz.views.generic import date_based
from libwaz.views.generic import create_update
from libwaz.contrib.object_permission.utils import generic_permission_check

from models import Category, Entry
from filtersets import EntryFilterSet
from forms import EntryForm, CategoryForm

PAGINATE_BY = 50

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

#
# Notice:
#    ブログアプリは`author`で絞り込む必要があるので独自に`permission_required`
#    を`generic_permission_check`を使用して定義しているが普通の汎用ビュー
#    の場合はこのような方法はナンセンス。`libwaz.contrib.object_permission.decorators`
#    にすでに`permission_required`というものが用意されているので特に絞り込みなどを行う必要
#    がない場合はそちらを使用すること。使い方は以下の`permission_required`と同一
#
def permission_required(perm, model=None):
    def wrapper(fn):
        def inner(request, *args, **kwargs):
            if not isinstance(kwargs['author'], User):
                author = get_object_or_404(User, username=kwargs['author'])
            else:
                author = kwargs['author']
            if model:
                queryset = model.objects.filter(author=author)
            else:
                queryset = None
            if not generic_permission_check(queryset, perm, request, *args, **kwargs):
                if request.user.is_authenticated():
                    raise Http403
                else:
                    return redirect_to_login(request.path)
            return fn(request, *args, **kwargs)
        return inner
    return wrapper
#
# object_filter
#----------------------------------------------------------------------------
@withauthor
def entry_filter(request, author, queryset=None, extra_context=None):
    if not queryset:
        queryset = Entry.objects.published(request)
    if author:
        queryset = queryset.filter(author=author)
    dict_info = dict(
        queryset        = queryset,
        filter_class    = EntryFilterSet,
        extra_context   = extra_context if extra_context else {'author': author},
    )
    return list_detail.object_filter(request, **dict_info)
#
# date_based
#----------------------------------------------------------------------------
@withauthor
def entry_archive_year(request, author, year, queryset=None):
    if not queryset:
        queryset = Entry.objects.published(request)
    if author:
        queryset = queryset.filter(author=author)
    dict_info = dict(
        queryset    = queryset,
        date_field  = 'publish_at',
        paginate_by = PAGINATE_BY,
        extra_context   = {'author': author},
    )
    return date_based.archive_year(request, year=year, **dict_info)
@withauthor
def entry_archive_month(request, author, year, month, queryset=None):
    if not queryset:
        queryset = Entry.objects.published(request)
    if author:
        queryset = queryset.filter(author=author)
    dict_info = dict(
        queryset        = queryset,
        date_field      = 'publish_at',
        month_format    = '%m',
        paginate_by     = PAGINATE_BY,
        extra_context   = {'author': author},
    )
    return date_based.archive_month(request, year=year, month=month, **dict_info)
@withauthor
def entry_archive_day(request, author, year, month, day, queryset=None):
    if not queryset:
        queryset = Entry.objects.published(request)
    if author:
        queryset = queryset.filter(author=author)
    dict_info = dict(
        queryset        = queryset,
        date_field      = 'publish_at',
        month_format    = '%m',
        paginate_by     = PAGINATE_BY,
        extra_context   = {'author': author},
    )
    return date_based.archive_day(request, year=year, month=month, day=day, **dict_info)
@withauthor
def entry_archive_today(request, author, queryset=None):
    if not queryset:
        queryset = Entry.objects.published(request)
    if author:
        queryset = queryset.filter(author=author)
    dict_info = dict(
        queryset        = queryset,
        date_field      = 'publish_at',
        month_format    = '%m',
        paginate_by     = PAGINATE_BY,
        extra_context   = {'author': author},
    )
    return date_based.archive_today(request, **dict_info)
@permission_required('blogs.view_entry', Entry)
@withauthor
def entry_detail(request, author, year, month, day, object_id):
    dict_info = dict(
        queryset        = Entry.objects.published(request).filter(author=author),
        date_field      = 'publish_at',
        month_format    = '%m',
        extra_context   = {'author': author},
    )
    return date_based.object_detail(request, year=year, month=month, day=day, object_id=object_id, **dict_info)

#
# create_update
#------------------------------------------------------------------------------
@permission_required('blogs.add_entry')
@withauthor
def create_entry(request, author):
    dict_info = dict(
        form_class     = EntryForm,
        extra_context   = {'author': author},
        initial_with_get = True,
    )
    if author != request.user and not request.user.is_superuser:
        raise Http403
    return create_update.create_object(request, **dict_info)
@permission_required('blogs.add_category')
@withauthor
def create_category(request, author):
    dict_info = dict(
        form_class      = CategoryForm,
        extra_context   = {'author': author},
        method          = 'json',
    )
    if author != request.user and not request.user.is_superuser:
        raise Http403
    return create_update.create_object(request, **dict_info)

@permission_required('blogs.change_entry', Entry)
@withauthor
def update_entry(request, author, object_id):
    dict_info = dict(
        form_class     = EntryForm,
        login_required = True,
        extra_context   = {'author': author},
    )
    return create_update.update_object(request, object_id=object_id, **dict_info)
@permission_required('blogs.change_category', Category)
@withauthor
def update_category(request, author, object_id):
    dict_info = dict(
        form_class     = CategoryForm,
        login_required = True,
        extra_context   = {'author': author},
        method          = 'json',
    )
    return create_update.update_object(request, object_id=object_id, **dict_info)

@permission_required('blogs.delete_entry', Entry)
@withauthor
def delete_entry(request, author, object_id):
    dict_info = dict(
        model                   = Entry,
        login_required          = True,
        post_delete_redirect    = reverse('blogs-entry-list', kwargs={'author': author}),
        extra_context           = {'author': author},
    )
    return create_update.delete_object(request, object_id=object_id, **dict_info)
@permission_required('blogs.delete_category', Category)
@withauthor
def delete_category(request, author, object_id):
    dict_info = dict(
        model                   = Category,
        login_required          = True,
        post_delete_redirect    = reverse('blogs-entry-list', kwargs={'author': author}),
        extra_context           = {'author': author},
        method                  = 'json',
    )
    return create_update.delete_object(request, object_id=object_id, **dict_info)