# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from django.contrib.auth.models import User
from libwaz.contrib.calls import site
from libwaz.contrib.calls.backends import BasicCallsBackend

from models import Announcement

class AnnouncementCallsBackend(BasicCallsBackend):
    MESSAGE = u"運営からのお知らせ: %(label)s"
    
    def autodiscover(self, instance, created, **kwargs):
        if instance.pub_state == 'draft' or instance.sage or not created:
            return
        users = User.objects.filter(is_active=True)
        for user_to in users:
            super(AnnouncementCallsBackend, self).autodiscover(instance=instance, created=created, user_to=user_to, **kwargs)
site.register(Announcement, AnnouncementCallsBackend)