# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if not hasattr(settings, 'TWITTER_SOURCE'):
    raise ImproperlyConfigured("You must define the TWITTER_SOURCE setting before using the `tweets` app.")
if not hasattr(settings, 'TWITTER_HASHTAGS'):
    raise ImproperlyConfigured("You must define the TWITTER_HASHTAGS setting before using the `tweets` app.")

settings.TWITTER_BODY_LENGTH_LIMIT = getattr(settings, 'TWITTER_BODY_LENGTH_LIMIT', 132)
settings.TWITTER_ENABLE = getattr(settings, 'TWITTER_ENABLE', True)