#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Utils for get default image url with seed


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
from django.conf import settings

PROFILE_ICON_PREFIX = r'profile_icon'
PROJECT_ICON_PREFIX = r'project_icon'
ADVERTISEMENT_IMG_PREFIX = r'advertisement_img'
GUEST_ICON_PREFIX = r'guest_icon'

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
