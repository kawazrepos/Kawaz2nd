# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/13
#
from django import template
from django.conf import settings as _settings

register = template.Library()

@register.simple_tag
def settings(name): 
    return str(_settings.__getattr__(name))