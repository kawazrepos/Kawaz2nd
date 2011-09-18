# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import striptags
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from libwaz.http import JsonResponse

import exceptions
from utils import parse_tag_input
from forms import MultiTagForm
from models import Tag, TaggedItem

def get_object_from_ct(content_type, object_id):
    u"""get object from `content_type` and `object_id`"""
    if settings.DEBUG:
        ctype = ContentType.objects.get(pk=content_type)
        obj = ctype.get_object_for_this_type(pk=object_id)
    else:
        ctype = get_object_or_404(ContentType, pk=content_type)
        try:
            obj = ctype.get_object_for_this_type(pk=object_id)
            return obj
        except ObjectDoesNotExist:
            raise Http404
    return obj

@login_required
@csrf_protect
@require_POST
def create_tags(request, *args, **kwargs):
    form = MultiTagForm(request.POST)
    if form.is_valid():
        obj = get_object_from_ct(form.cleaned_data['content_type'], form.cleaned_data['object_id'])
        instance_list = []
        errors = []
        for label in parse_tag_input(form.cleaned_data['labels']):
            try:
                tagged_item = Tag.objects.add_tag(obj, label, ignore_duplicate=False)
                instance_list.append(tagged_item.json())
            except exceptions.DuplicateError:
                errors.append(_(u"Tag %(label)s is duplicated.") % {'label': label})
        data = {
            'status':           'ok',
            'instance_list':    instance_list,
        }
        if len(errors) > 0: data['errors'] = errors
        return JsonResponse(data)
    else:
        errors = [unicode(striptags("%s: %s" % (k, v))) for k, v in form.errors.iteritems()]
        return JsonResponse({'status': 'failed', 'errors': errors})

@login_required
@csrf_protect
@require_POST
def sort_tags(request, *args, **kwargs):
    form = MultiTagForm(request.POST)
    if form.is_valid():
        instance_list = []
        errors = []
        obj = get_object_from_ct(form.cleaned_data['content_type'], form.cleaned_data['object_id'])
        for i, label in enumerate(parse_tag_input(form.cleaned_data['labels'])):
            tagged_item = Tag.objects.add_tag(obj, label)
            tagged_item.order = i
            tagged_item.save()
            instance_list.append(tagged_item.json())
        data = {
            'status':           'ok',
            'instance_list':    instance_list,
        }
        return JsonResponse(data)
    else:
        errors = [unicode(striptags("%s: %s" % (k, v))) for k, v in form.errors.iteritems()]
        return JsonResponse({'status': 'faield', 'errors': errors})
    
@login_required
@csrf_protect
@require_POST
def delete_tags(request, *args, **kwargs):
    form = MultiTagForm(request.POST)
    if form.is_valid():
        instance_list = []
        errors = []
        obj = get_object_from_ct(form.cleaned_data['content_type'], form.cleaned_data['object_id'])
        for label in parse_tag_input(form.cleaned_data['labels']):
            try:
                tagged_item = Tag.objects.remove_tag(obj, label)
                instance_list.append(tagged_item.json())
            except exceptions.DeletingFrozenTagError:
                errors.append(_(u"Unable to delete Tag %(label)s while it is frozen.") % {'label': label})
            except (Tag.DoesNotExist, TaggedItem.DoesNotExist):
                errors.append(_(u"Tag %(label)s is not defined.") % {'label': label})
        data = {
            'status':           'ok',
            'instance_list':    instance_list,
        }
        if len(errors) > 0: data['errors'] = errors
        return JsonResponse(data)
    else:
        errors = [unicode(striptags("%s: %s" % (k, v))) for k, v in form.errors.iteritems()]
        return JsonResponse({'status': 'faield', 'errors': errors})

@login_required
@csrf_protect
@require_POST
def freeze_tags(request, *args, **kwargs):
    form = MultiTagForm(request.POST)
    if form.is_valid():
        instance_list = []
        errors = []
        obj = get_object_from_ct(form.cleaned_data['content_type'], form.cleaned_data['object_id'])
        # Validation
        if getattr(obj, 'author', None) != request.user and getattr(obj, 'user', None) != request.user:
            return JsonResponse({'status': 'failed', 'errors': [_('Permission denied')]})
        for label in parse_tag_input(form.cleaned_data['labels']):
            try:
                tagged_item = Tag.objects.freeze_tag(obj, label)
                instance_list.append(tagged_item.json())
            except (Tag.DoesNotExist, TaggedItem.DoesNotExist):
                errors.append(_(u"Tag %(label)s is not defined.") % {'label': label})
        data = {
            'status':           'ok',
            'instance_list':    instance_list,
        }
        if len(errors) > 0: data['errors'] = errors
        return JsonResponse(data)
    else:
        errors = [unicode(striptags("%s: %s" % (k, v))) for k, v in form.errors.iteritems()]
        return JsonResponse({'status': 'faield', 'errors': errors})