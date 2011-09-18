# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from django.core.urlresolvers import reverse

from libwaz.views.generic import list_detail
from libwaz.views.generic import date_based
from libwaz.views.generic import create_update
from libwaz.contrib.object_permission.decorators import permission_required

from forms import AnnouncementForm
from models import Announcement

#
# list_detail
#---------------------------------------------------------------------------------
def announcement_list(request):
    kwargs = {
        'queryset': Announcement.objects.published(request),
        'paginate_by': 200,
    }
    return list_detail.object_list(request, **kwargs)
@permission_required('announcements.view_announcement', Announcement)
def announcement_detail(request, object_id):
    kwargs = {
        'queryset': Announcement.objects.published(request),
    }
    return list_detail.object_detail(request, object_id=object_id, **kwargs)

#
# date_based
#----------------------------------------------------------------------------------
def announcement_archive_year(request, year):
    kwargs = {
        'queryset':     Announcement.objects.published(request),
        'date_field':   'updated_at',
        'allow_empty':  True,
    }
    return date_based.archive_year(request, year=year, **kwargs)
def announcement_archive_month(request, year, month):
    kwargs = {
        'queryset':     Announcement.objects.published(request),
        'date_field':   'updated_at',
        'month_format': '%m',
        'allow_empty':  True,
        'paginate_by': 200,
    }
    return date_based.archive_month(request, year=year, month=month, **kwargs)

#
# create_update
#-----------------------------------------------------------------------------------
@permission_required('announcements.add_announcement')
def create_announcement(request):
    kwargs = {
        'form_class': AnnouncementForm,
    }
    return create_update.create_object(request, **kwargs)

@permission_required('announcements.change_announcement', Announcement)
def update_announcement(request, object_id):
    kwargs = {
        'form_class': AnnouncementForm,
    }
    return create_update.update_object(request, object_id=object_id, **kwargs)

@permission_required('announcements.delete_announcement', Announcement)
def delete_announcement(request, object_id):
    kwargs = {
        'model': Announcement,
        'post_delete_redirect': reverse('announcements-announcement-list')
    }
    return create_update.delete_object(request, object_id=object_id, **kwargs)
