# -*- coding: utf-8 -*-
#
# Author:    alisue
# Date:      2010/10/31
#
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.views.generic import simple

from libwaz.views.decorators.auth import staff_required, superuser_required

import forms
from utils import resave

@staff_required
def index(request):
    kwargs = {
        'template': 'utilities/index.html'
    }
    return simple.direct_to_template(request, **kwargs)

@staff_required
def template_check(request, template):
    kwargs = {
        'template': template,
    }
    return simple.direct_to_template(request, **kwargs)

@superuser_required
def configure(request):
    kwargs = {
        'template': 'utilities/configure.html',
        'extra_context': {
            'settings': settings._wrapped.__dict__,
        }
    }
    return simple.direct_to_template(request, **kwargs)

@csrf_protect
@staff_required
def email(request):
    from django.contrib.sites.models import RequestSite
    from django.contrib.sites.models import Site
    if request.method == 'POST':
        form = forms.EmailUsersForm(request.POST)
        if form.is_valid():
            recivers = form.cleaned_data['recivers']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            
            if Site._meta.installed:
                site = Site.objects.get_current()
            else:
                site = RequestSite(request)
            
            for reciver in recivers:
                ctx_dict = {'site': site, 'sender': request.user, 'reciver': reciver, 'subject': subject, 'body': body}
                subject = render_to_string('utilities/email_subject.txt', ctx_dict)
                # Email subject *must not* contain newlines
                subject = ''.join(subject.splitlines())
                msg = render_to_string('utilities/email.txt', ctx_dict)
                reciver.email_user(subject, msg)
            messages.success(request, u"メールの送信をしました", fail_silently=True)
    else:
        to = request.GET.get('to', None)
        if to:
            to = get_object_or_404(User, username=to)
            form = forms.EmailUsersForm(initial={'recivers': [to.pk]})
        else:
            form = forms.EmailUsersForm()
    kwargs = {
        'template': r'utilities/email_form.html',
        'extra_context': {
            'form': form
        }
    }
    return simple.direct_to_template(request, **kwargs)

@csrf_protect
@superuser_required
def resave_all(request):
    if request.method == 'POST':
        count = resave.resave()
        status = u"%d個のオブジェクトを再保存しました" % count
    else:
        status = None
    kwargs = {
        'template': r'utilities/resave_all.html',
        'extra_context': {
            'status': status, 'natural_keys': resave.RESAVE_WHITE_LIST
        },
    }
    return simple.direct_to_template(request, **kwargs)

@csrf_protect
@superuser_required
def remodify_object_permission(request):
    if request.method == 'POST':
        import os, commands
        manage = os.path.join(os.path.dirname(__file__), '../manage.py')
        status, output = commands.getstatusoutput('python %s remodify_object_permission' % manage)
    else:
        status, output = None, None
    kwargs = {
        'template': r'utilities/remodify_object_permission.html',
        'extra_context': {
            'status': status,
            'output': output
        },
    }
    return simple.direct_to_template(request, **kwargs)

@csrf_protect
@superuser_required
def fixture(request, format='yaml'):
    if request.method == 'POST':
        if 'format' in request.REQUEST:
            format = request.REQUEST['format']
        import os, commands
        if format == 'sql':
            database = settings.DATABASES['default']
            engine = database['ENGINE']
            if engine == 'django.db.backends.sqlite3':
                import os.path
                status = 0
                output = open(os.path.join('../', database['NAME'])).read()
            elif engine == 'django.db.backends.mysql':
                name = database['NAME']
                user = database['USER']
                pswd = database['PASSWORD']
                status, output = commands.getstatusoutput('mysqldump -u %s -p%s %s' % (user, pswd, name))
        else:
            manage = os.path.join(os.path.dirname(__file__), '../manage.py')
            status, output = commands.getstatusoutput('python %s dumpdata --format %s' % (manage, format))
        if status == 0:
            response = HttpResponse(output)
            response['Cache-Control'] = 'no-cache'
            response['Content-Disposition'] = 'attachment; filename=dump.%s' % format
            return response
    else:
        status = None
        output = None
    kwargs = {
        'template': r'utilities/fixture.html',
        'extra_context': {
            'status': status,
            'output': output
        },
    }
    return simple.direct_to_template(request, **kwargs)
