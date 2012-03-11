# -*- coding: utf-8 -*-
# Create required permission
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
ct = ContentType.objects.get_for_model(User)
kwargs = {
        'content_type': ct,
        'codename': 'post_goforit',
        'name': u"ネタパーミッション",
    }
Permission.objects.get_or_create(**kwargs)

