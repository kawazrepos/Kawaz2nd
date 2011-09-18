# -*- coding: utf-8 -*-
from django import template
from django.contrib.auth.models import User

from ..models import Task
from ...projects.models import Project

register = template.Library()

class GetAvariableStatusListOfForAs(template.Node):
    def __init__(self, task, user, variable_name):
        self.task, self.user, self.variable_name = task, user, variable_name
    
    def render(self, context):
        task = self.task.resolve(context)
        user = self.user.resolve(context)
        context[self.variable_name] = task.get_avariable_status_list(user)
        return ''
@register.tag
def get_avariable_status_list(parser, token):
    u"""
    特定タスクが特定ユーザーが現在有効なステータスのリストを返す
    
    Usage:
        get_abariable_status_list of <task> for <user> as <variable>
    """
    bits = token.split_contents()
    if len(bits) == 7:
        if bits[1] != 'of':
            raise template.TemplateSyntaxError("first argument of %r has to be 'of'" % bits[0])
        elif bits[3] != 'for':
            raise template.TemplateSyntaxError("third argument of %r has to be 'for'" % bits[0])
        elif bits[5] != 'as':
            raise template.TemplateSyntaxError("fifth argument of %r has to be 'as'" % bits[0])
        task = parser.compile_filter(bits[2])
        user = parser.compile_filter(bits[4])
        variable_name = bits[6]
    else:
        raise template.TemplateSyntaxError("%r has to be written as 'get_abariable_status_list of <task> for <user> as <variable>`" % bits[0])
    return GetAvariableStatusListOfForAs(task, user, variable_name)


class GetStatusTaskCountForAs(template.Node):
    def __init__(self, request, project_or_user, variable_name, include, exclude):
        self.request, self.project_or_user = request, project_or_user
        self.variable_name = variable_name
        self.include, self.exclude = include, exclude
    def render(self, context):
        request = self.request.resolve(context)
        project_or_user = self.project_or_user.resolve(context)
        qs = Task.objects.published(request)
        if isinstance(project_or_user, User):
            qs = qs.filter(owners=project_or_user)
        else:
            qs = qs.filter(project=project_or_user)
        if self.include:
            qs = qs.filter(status__in=self.include)
        if self.exclude:
            qs = qs.exclude(status__in=self.exclude)
        context[self.variable_name] = qs.count()
        return ''
class GetStatusTaskListForAs(template.Node):
    def __init__(self, request, project_or_user, variable_name, include, exclude):
        self.request, self.project_or_user = request, project_or_user
        self.variable_name = variable_name
        self.include, self.exclude = include, exclude
    def render(self, context):
        request = self.request.resolve(context)
        qs = Task.objects.published(request)
        if self.project_or_user:
            project_or_user = self.project_or_user.resolve(context)
            if isinstance(project_or_user, User):
                qs = qs.filter(owners=project_or_user)
            else:
                qs = qs.filter(project=project_or_user)
        if self.include:
            qs = qs.filter(status__in=self.include)
        if self.exclude:
            qs = qs.exclude(status__in=self.exclude)
        context[self.variable_name] = qs
        return ''
def get_status_task_base(parser, token, Node, include=None, exclude=None):
    u"""
    タスクの個数・リストを返すタグのスーパー関数
    """
    bits = token.split_contents()
    if len(bits) == 6:
        # get_status_task_count <request> for <project or user> as <variable>
        if bits[2] != 'for':
            raise template.TemplateSyntaxError("second argument of %r has to be 'for'" % bits[0])
        elif bits[4] != 'as':
            raise template.TemplateSyntaxError("fourth argument of %r has to be 'as'" % bits[0])
        request = parser.compile_filter(bits[1])
        project_or_user = parser.compile_filter(bits[3])
        variable_name = bits[5]
    else:
        raise template.TemplateSyntaxError("%(tag)r has to be written as '%(tag)r <request> for <project or user> as <variable>'" % {'tag':bits[0]})
    return Node(request, project_or_user, variable_name, include, exclude)
def get_status_task_count(parser, token, include=None, exclude=None):
    u"""
    `include`と`exclude`で指定されたステータスを持つタスクの個数を返す
    """
    return get_status_task_base(parser, token, GetStatusTaskCountForAs, include, exclude)
def get_status_task_list(parser, token, include=None, exclude=None):
    u"""
    `include`と`exclude`で指定されたステータスを持つタスクのリストを返す
    """
    return get_status_task_base(parser, token, GetStatusTaskListForAs, include, exclude)

@register.tag
def get_active_task_count(parser, token):
    u"""
    現在有効なタスクの個数を返す
    
    Usage:
        get_active_task_count <request> for <project or user> as <variable>
    """
    return get_status_task_count(parser, token, include=['new', 'rejected', 'accepted', 'paused'])
@register.tag
def get_active_task_list(parser, token):
    u"""
    現在有効なタスクのリストを返す
    
    Usage:
        get_active_task_list <request> for <project or user> as <variable>
    """
    return get_status_task_list(parser, token, include=['new', 'rejected', 'accepted', 'paused'])
@register.tag
def get_progress_task_list(parser, token):
    u"""
    現在進行中のタスクのリストを返す
    
    Usage:
        get_active_task_list <request> for <project or user> as <variable>
    """
    return get_status_task_list(parser, token, include=['accepted', 'paused'])

@register.tag
def get_unaccepted_task_count(parser, token):
    u"""
    確認していないタスクの個数を返す
    
    Usage:
        get_unaccepted_task_count <request> for <project or user> as <variable>
    """
    return get_status_task_count(parser, token, include=['new', 'rejected'])

@register.tag
def get_progress_task_count(parser, token):
    u"""
    現在進行中のタスクの個数を返す
    
    Usage:
        get_progress_task_count <request> for <project or user> as <variable>
    """
    return get_status_task_count(parser, token, include=['accepted', 'paused'])
