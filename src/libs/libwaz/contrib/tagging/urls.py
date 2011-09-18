# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from models import Tag
import views

dict_info = {
    'queryset':     Tag.objects.all(),
}
urlpatterns = patterns('libwaz.views.generic.json.list_detail',
    (r'^sort/$',            views.sort_tags,    {},                                     'tagging-tag-sort'),
    (r'^create/$',          views.create_tags,  {},                                     'tagging-tag-create'),
    (r'^delete/$',          views.delete_tags,  {},                                     'tagging-tag-delete'),
    (r'^freeze/$',          views.freeze_tags,  {},                                     'tagging-tag-freeze'),
    (r'^(?P<slug>[^/]+)/$', 'object_detail',    dict(dict_info, slug_field='label'),    'tagging-tag-detail'),
    (r'^$',                 'object_list',      dict_info,                              'tagging-tag-list'),
)