# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/08
#
from models import PermissionGroup

#
# Warning:
#    DjangoのAuthアプリで使用されている`is_staff`のDB上の値はこのミドルウェアにより上書きされる
#
class PermissionGroupMiddleware(object):
    def process_request(self, request):
        if not hasattr(request, 'user'):
            raise RuntimeError(u"This middleware has to be called after 'django.contrib.auth.middleware.AuthenticationMiddleware'")
        promotable_permission_groups = PermissionGroup.objects.filter(is_promotable=True)
        promotable_groups = [permission_group.group for permission_group in promotable_permission_groups]
        is_promotable = False
        for group in promotable_groups:
            if group in request.user.groups.all():
                is_promotable=True
                break
        staff_permission_groups = PermissionGroup.objects.filter(is_staff=True)
        staff_groups = [permission_group.group for permission_group in staff_permission_groups]
        is_staff = False
        for group in staff_groups:
            if group in request.user.groups.all():
                is_staff=True
                break
        request.user.is_promotable = is_promotable
        request.user.is_staff = is_staff
        return None