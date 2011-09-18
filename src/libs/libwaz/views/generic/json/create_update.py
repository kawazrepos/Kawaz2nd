# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/24
#
# Notice:
#    ユーザーに対してメッセージを送るコードがコメントアウトされているが
#    Ajaxリクエストで作成した場合ページ遷移が無くメッセージが表示されること
#    無くたまってしまう。したがってAjaxでモデルを複数個作成などしたあとで
#    ページ遷移を行うと溜まっていたメッセージが一度に表示されてしまいウザイ
#    なのでコメントアウトしてある
#
#from django.contrib import messages
#from django.utils.translation import ugettext
from django.template.defaultfilters import striptags
#import django.views.generic.create_update
from libwaz.views.generic.withrequest import create_update

from libwaz.http import JsonResponse
from decorators import hand_response_method_to_kwargs
from utils import get_instance_json

from libwaz.forms import ModelFormWithRequest
from libwaz.db.models import ModelWithRequest

class JsonGenericViewError(Exception):
    """A problem in a generic view."""
    pass


@hand_response_method_to_kwargs
def create_object(request, method='json', *args, **kwargs):
    if method == 'json' and request.method == 'POST':
        login_required = kwargs.get('login_required')
        model = kwargs.get('model')
        form_class = kwargs.get('form_class')
        if login_required and not request.user.is_authenticated():
            return JsonResponse({'status': 'denied'})
        model, form_class = create_update.get_model_and_form_class(model, form_class)
        if request.method == 'POST':
            if issubclass(form_class, ModelFormWithRequest):
                form = form_class(request, request.POST, request.FILES)
            else:
                form = form_class(request.POST, request.FILES)
            if form.is_valid():
                new_object = form.save()
                #msg = ugettext("The %(verbose_name)s was created successfully.") %\
                #                    {"verbose_name": model._meta.verbose_name}
                #messages.success(request, msg, fail_silently=True)
                return JsonResponse({'status': 'ok', 'instance': get_instance_json(new_object)})
            else:
                errors = [unicode(striptags("%s: %s" % (k, v))) for k, v in form.errors.iteritems()]
                return JsonResponse({'status': 'failed', 'errors': errors})
    else:
        return create_update.create_object(request, *args, **kwargs)

@hand_response_method_to_kwargs
def update_object(request, method='json', *args, **kwargs):
    if method == 'json' and request.method == 'POST':
        login_required = kwargs.get('login_required')
        model = kwargs.get('model')
        form_class = kwargs.get('form_class')
        object_id = kwargs.get('object_id')
        slug = kwargs.get('slug')
        slug_field = kwargs.get('slug_field', 'slug')
        if login_required and not request.user.is_authenticated():
            return JsonResponse({'status': 'denied'})
        model, form_class = create_update.get_model_and_form_class(model, form_class)
        obj = create_update.lookup_object(model, object_id, slug, slug_field)
        if request.method == 'POST':
            if issubclass(form_class, ModelFormWithRequest):
                form = form_class(request, request.POST, request.FILES, instance=obj)
            else:
                form = form_class(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                obj = form.save()
                #msg = ugettext("The %(verbose_name)s was updated successfully.") %\
                #                    {"verbose_name": model._meta.verbose_name}
                #messages.success(request, msg, fail_silently=True)
                return JsonResponse({'status': 'ok', 'instance': get_instance_json(obj)})
            else:
                errors = [unicode(striptags("%s: %s" % (k, v))) for k, v in form.errors.iteritems()]
                return JsonResponse({'status': 'failed', 'errors': errors})
    else:
        return create_update.update_object(request, *args, **kwargs)

@hand_response_method_to_kwargs
def delete_object(request, method='json', *args, **kwargs):
    if method == 'json' and request.method == 'POST':
        login_required = kwargs.get('login_required')
        model = kwargs['model']
        post_delete_redirect = kwargs['post_delete_redirect']
        object_id = kwargs.get('object_id')
        slug = kwargs.get('slug')
        slug_field = kwargs.get('slug_field', 'slug')
        if login_required and not request.user.is_authenticated():
            return JsonResponse({'status': 'denied'})
        obj = create_update.lookup_object(model, object_id, slug, slug_field)
        if request.method == 'POST':
            if isinstance(obj, ModelWithRequest):
                obj.delete(request)
            else:
                obj.delete()
            #msg = ugettext("The %(verbose_name)s was deleted.") %\
            #                        {"verbose_name": model._meta.verbose_name}
            #messages.success(request, msg, fail_silently=True)
            return JsonResponse({'status': 'ok', 'post_delete_redirect': u"%s"%post_delete_redirect})
    else:
        return create_update.delete_object(request, *args, **kwargs)