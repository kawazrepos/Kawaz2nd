# -*- coding: utf-8 -*-
from django.conf import settings

settings.MAX_TAG_LENGTH = getattr(settings, 'MAX_TAG_LENGTH', 50)