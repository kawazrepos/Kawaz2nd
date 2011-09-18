# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/24
#
def get_instance_json(instance):
    value = getattr(instance, 'json', {})
    if callable(value): value = value()
    if isinstance(value, dict):
        if not 'pk' in value:
            value['pk'] = instance.pk
    return value