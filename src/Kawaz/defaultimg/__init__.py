# -*- coding: utf-8 -*-
#
# @author:    alisue
# @date:        2010/10/24
#
from django.conf import settings

import random

PROFILE_ICON_PREFIX         = r'profile_icon'
PROJECT_ICON_PREFIX         = r'project_icon'
ADVERTISEMENT_IMG_PREFIX    = r'advertisement_img'
GUEST_ICON_PREFIX           = r'guest_icon'

def _get(size, seed, prefix, max):
    filename = "%s.%s.%02d.png" % (
        prefix,
        size.lower(),
        seed % max + 1,
    )
    return "%simage/default/%s" % (settings.MEDIA_URL, filename)

def get_default_profile_icon(size, seed):
    return _get(size, seed, PROFILE_ICON_PREFIX, 6)

def get_default_project_icon(size, seed):
    return _get(size, seed, PROJECT_ICON_PREFIX, 1)

def get_default_guest_icon(size, seed):
    return _get(size, seed, GUEST_ICON_PREFIX, 12)

def get_default_advertisement_img(size, seed):
    return _get(size, seed, ADVERTISEMENT_IMG_PREFIX, 1)