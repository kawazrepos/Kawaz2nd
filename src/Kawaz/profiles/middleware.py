# -*- coding: utf-8 -*-
#
# Created:    2010/09/27
# Author:         alisue
#
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import MiddlewareNotUsed

import django.views.static
import django.contrib.auth.views

IGNORE_REDIRECTION_VIEWS = (
    django.views.static.serve,
    django.contrib.auth.views.logout,
)
class RedirectIfProfileHasNotConfiguredMiddleware(object):
    u"""ユーザーのプロフィールが更新されていない場合は強制的にプロフィール更新ページに移動させる"""
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if not hasattr(request, 'user'):
                raise RuntimeError(u"This middleware has to be called after 'django.contrib.auth.middleware.AuthenticationMiddleware'")
            elif view_func in IGNORE_REDIRECTION_VIEWS:
                return None
            if request.user.is_authenticated():
                profile = request.user.get_profile()
                url = reverse('profiles-profile-update')
                if not profile.nickname and request.path != url:
                    # まだユーザーのプロフィールが更新されていないのでプロフィール更新ページに強制的に移動させる
                    return HttpResponseRedirect(url)
        except:
            # Fail silently
            pass
        return None
