# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/08
#
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

RESAVE_WHITE_LIST = settings.RESAVE_WHITE_LIST
RESAVE_BLACK_LIST = settings.RESAVE_BLACK_LIST

def _resave(model, callback=None):
    for i, obj in enumerate(model.objects.all()):
        obj.save()
        if callback: callback(model=model, index=i, instance=obj)
    return model.objects.count()

def _model_list(whitelist=RESAVE_WHITE_LIST, blacklist=RESAVE_BLACK_LIST):
    model_list = []
    content_types = ContentType.objects.all()
    for ct in content_types:
        natural_key = ".".join(ct.natural_key())
        if whitelist and not natural_key in whitelist:
            continue
        if blacklist and natural_key in blacklist:
            continue
        model_list.append(ct.model_class())
    return model_list

def resave(model=None, callback=None, whitelist=RESAVE_WHITE_LIST, blacklist=RESAVE_BLACK_LIST):
    # Historyを停止
    settings.HISTORY_ENABLE = False
    if model is None:
        model_list = _model_list(whitelist, blacklist)
        count = 0
        for model in model_list:
            count += _resave(model, callback)
    else:
        count = _resave(model, callback)
    # Historyを再開
    settings.HISTORY_ENABLE = True
    return count