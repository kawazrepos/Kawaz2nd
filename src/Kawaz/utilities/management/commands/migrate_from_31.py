# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from django.core.management.base import NoArgsCommand

from libwaz.contrib.history.models import Timeline
from libwaz.contrib.history import exceptions
from libwaz.contrib.history import site

from Kawaz.mcomments.models import MarkItUpComment

class Command(NoArgsCommand):
    help = u"Kawaz ver 0.31からHell Brunchへのマイグレーション用ツール"
    
    def handle_noargs(self, **options):
        output = []
        # History Timeline
        qs = Timeline.objects.filter(url='')
        remove_list = []
        for timeline in qs:
            try:
                instance = timeline.content_object
                if instance is None:
                    remove_list.append(timeline.pk)
                elif getattr(instance, 'pub_state', 'public') == 'draft':
                    remove_list.append(timeline.pk)
                else:
                    try:
                        backend = site.get_backend(instance.__class__)
                        timeline.url = backend._get_url_from_instance(instance)
                        timeline.save()
                    except exceptions.NotRegistered:
                        # Backendが登録されていないため破棄
                        remove_list.append(timeline.pk)
            except AttributeError:
                remove_list.append(timeline.pk)
        Timeline.objects.filter(pk__in=remove_list).delete()
        # Comment
        qs = MarkItUpComment.objects.all()
        remove_list = []
        for comment in qs:
            try:
                instance = comment.content_object
                if instance is None:
                    remove_list.append(comment.pk)
            except AttributeError:
                remove_list.append(comment.pk)
        MarkItUpComment.objects.filter(pk__in=remove_list).delete()
        return "\n".join(output)