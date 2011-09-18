# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/25
#
from django.conf.urls.defaults import *

import views

components_patterns = patterns('',
    url(r'^$',                              views.component_list,       name='bugwaz-component-list'),
    url(r'^(?P<object_id>\d+)/$',           views.component_detail,     name='bugwaz-component-detail'),
    url(r'^create/$',                       views.create_component,     name='bugwaz-component-create'),
    url(r'^(?P<object_id>\d+)/update/$',    views.update_component,     name='bugwaz-component-update'),
    url(r'^(?P<object_id>\d+)/delete/$',    views.delete_component,     name='bugwaz-component-delete'),
)
versions_patterns = patterns('',
    url(r'^$',                              views.version_list,         name='bugwaz-version-list'),
    url(r'^(?P<object_id>\d+)/$',           views.version_detail,       name='bugwaz-version-detail'),
    url(r'^create/$',                       views.create_version,       name='bugwaz-version-create'),
    url(r'^(?P<object_id>\d+)/update/$',    views.update_version,       name='bugwaz-version-update'),
    url(r'^(?P<object_id>\d+)/delete/$',    views.delete_version,       name='bugwaz-version-delete'),
)
reports_patterns = patterns('',
    url(r'^$',                                  views.report_list,          name='bugwaz-report-list'),
    url(r'^(?P<object_id>\d+)/$',               views.report_detail,        name='bugwaz-report-detail'),
    url(r'^create/$',                           views.create_report,        name='bugwaz-report-create'),
    url(r'^(?P<object_id>\d+)/update/$',        views.update_report,        name='bugwaz-report-update'),
    url(r'^(?P<object_id>\d+)/update_status/$', views.update_report_status, name='bugwaz-report-update-status'),
    url(r'^(?P<object_id>\d+)/delete/$',        views.delete_report,        name='bugwaz-report-delete'),
    url(r'^(?P<object_id>\d+)/charge/$',        views.charge_report,        name='bugwaz-report-charge'),
    url(r'^(?P<object_id>\d+)/discharge/$',     views.discharge_report,     name='bugwaz-report-discharge'),
)
extra_patterns = patterns('',
    (r'^components/',                       include(components_patterns)),
    (r'^versions/',                         include(versions_patterns)),
    (r'^reports/',                          include(reports_patterns)),
)
urlpatterns = patterns('',
    url(r'^$',                              views.product_list,         name='bugwaz-product-list'),
    url(r'^(?P<object_id>\d+)/$',           views.product_detail,       name='bugwaz-product-detail'),
    url(r'^create/$',                       views.create_product,       name='bugwaz-product-create'),
    url(r'^(?P<object_id>\d+)/update/$',    views.update_product,       name='bugwaz-product-update'),
    url(r'^(?P<object_id>\d+)/delete/$',    views.delete_product,       name='bugwaz-product-delete'),
    (r'^(?P<product>\d+)/',                 include(extra_patterns)),
)