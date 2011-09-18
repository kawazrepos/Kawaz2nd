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
site.register(MarkItUpComment, CommentHistoryBackend)