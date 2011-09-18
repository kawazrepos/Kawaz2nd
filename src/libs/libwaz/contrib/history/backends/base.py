# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

USER_ATTRS = (
    'updated_by',
    'author',
    'user',
)

class BaseHistoryBackend(object):
    u"""
    Generic backend for history application
    """
    def setUp(self, model):
        pass
    def tearDown(self, model):
        pass
    
    def get_user(self, timeline):
        u"""
        get user name from auth.user object with permalink
        """
        if timeline.user and timeline.user.is_authenticated():
            if hasattr(timeline.user, 'get_profile'):
                kwargs = {
                    'href':     timeline.user.get_profile().get_absolute_url(),
                    'title':    timeline.user.get_profile().__unicode__(),
                    'label':    timeline.user.get_profile().__unicode__(),
                }
            else:
                kwargs = {
                    'href':     timeline.user.get_absolute_url(),
                    'title':    timeline.user.__unicode__(),
                    'label':    timeline.user.__unicode__(),
                }
            return mark_safe(u"""<a href="%(href)s" title="%(title)s">%(label)s</a>""" % kwargs)
        else:
            return _("Anonymous User")
        
    def get_label(self, timeline):
        kwargs = {
            'href':     timeline.url,
            'label':    timeline.label,
        }
        return mark_safe(u"""<a href="%(href)s">%(label)s</a>""" % kwargs)
    
    def _get_url_from_instance(self, instance):
        if instance is None:
            return ''
        return instance.get_absolute_url()
    def _get_label_from_instance(self, instance):
        if instance is None:
            return ''
        return instance.__unicode__()
    def _get_user_from_instance(self, instance):
        if instance is None:
            return ''
        for attr in USER_ATTRS:
            user = getattr(instance, attr, None)
            if user: break
        return user
    
    def get_message(self, timeline):
        u"""
        get message for timeline object from content_object with permalinks
        """
        kwargs = {
            'user':     self.get_user(timeline),
            'label':    self.get_label(timeline),
        }
        if timeline.action == 'create':
            return mark_safe(_(u"""%(user)s create '%(label)s'""") % kwargs)
        elif timeline.action == 'update':
            return mark_safe(_(u"""%(user)s update '%(label)s'""") % kwargs)
        return mark_safe(_(u"""%(user)s delete '%(label)s'""") % kwargs)
    
    def autodiscover(self, instance, action, url=None, label=None, user=None):
        raise NotImplementedError