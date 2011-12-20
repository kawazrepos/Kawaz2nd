# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/27
#
# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/11
#
from libwaz.contrib.history import site
from libwaz.contrib.history.backends import CommentHistoryBackend
from models import MarkItUpComment

class MarkItUpCommentHistoryBackend(CommentHistoryBackend):
    def autodiscover(self, instance, *args, **kwargs):
        if not instance.is_public:
            return None
        return super(MarkItUpCommentHistoryBackend, self).autodiscover(instance, *args, **kwargs)
site.register(MarkItUpComment, MarkItUpCommentHistoryBackend)
