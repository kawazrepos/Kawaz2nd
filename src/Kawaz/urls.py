# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

# Include Application
#--------------------------------------------------------------------------------
urlpatterns = patterns('',
    # Admin site
    (r'^central-dogma/doc/',                    include('django.contrib.admindocs.urls')),
    (r'^central-dogma/',                        include(admin.site.urls)),
    # Contrib
    (r'^comments/',                             include('Kawaz.mcomments.urls')),
    (r'^search/',                               include('haystack.urls')),
    # Applications
    (r'^trackback/',                            include('libwaz.contrib.trackback.urls')),
    (r'^drafts/',                               include('libwaz.contrib.drafts.urls')),
    (r'^permissiongroups/',                     include('Kawaz.permissiongroups.urls')),
    (r'^registration/',                         include('Kawaz.threestep_registration.urls')),
    (r'^history/',                              include('libwaz.contrib.history.urls')),
    (r'^commons/',                              include('Kawaz.commons.urls')),
    (r'^events/',                               include('Kawaz.events.urls')),
    (r'^tweets/',                               include('Kawaz.tweets.urls')),
    (r'^threads/',                              include('Kawaz.threads.urls')),
    (r'^messages/',                             include('Kawaz.messages.urls')),
    (r'^tasks/',                                include('Kawaz.tasks.urls')),
    (r'^projects/',                             include('Kawaz.projects.urls')),
    (r'^projects/(?P<project>[^/]+)/wikis/',    include('Kawaz.wikis.urls')),
    (r'^announcements/',                        include('Kawaz.announcements.urls')),
    (r'^tags/',                                 include('libwaz.contrib.tagging.urls')),
    (r'^',                                      include('Kawaz.index.urls')),
    (r'^members/',                              include('Kawaz.profiles.urls')),
    (r'^blogs/',                                include('Kawaz.blogs.urls')),
    (r'^bugwaz/',                               include('Kawaz.bugwaz.urls')),
    (r'^utilities/',                            include('Kawaz.utilities.urls')),
    (r'^contact/',                              include('Kawaz.contact.urls')),
    (r'^calls/',                                include('libwaz.contrib.calls.urls')),
    (r'^star/',                                 include('libwaz.contrib.star.api.urls')),
)

#
# MarkItUpFieldでPreviewを行うためのビュー定義
#
def apply_filter(request):
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    from utils.markups import markdown
    markup = markdown(request.POST.get('data', ''))
    return render_to_response('preview.html', {'markup': markup}, RequestContext(request))
urlpatterns += patterns('',
    (r'^preview/',      apply_filter,   {}, 'preview'),
)
from django.conf import settings
if settings.DEBUG:
    #
    # プロダクトの静的ファイルの提供はApatchなどで行う
    #    Ref. http://djangoproject.jp/doc/ja/1.0/howto/static-files.html
    #
    import os.path
    document_root = lambda x: os.path.join(os.path.dirname(__file__), x)
    urlpatterns += patterns('django.views.static',
        (r'^favicon.ico$',              'serve', {'document_root': document_root('../../statics'), 'path': 'favicon.ico'}),
        (r'^apple-touch-icon.png$',     'serve', {'document_root': document_root('../../statics'), 'path': 'apple-touch-icon.png'}),
        (r'^css/(?P<path>.*)$',         'serve', {'document_root': document_root('../../statics/css')}),
        (r'^javascript/(?P<path>.*)$',  'serve', {'document_root': document_root('../../statics/javascript')}),
        (r'^image/(?P<path>.*)$',       'serve', {'document_root': document_root('../../statics/image')}),
        (r'^storage/(?P<path>.*)$',     'serve', {'document_root': document_root('../../statics/storage')}),
        (r'^component/(?P<path>.*)$',   'serve', {'document_root': document_root('../../statics/component')}),
    )
