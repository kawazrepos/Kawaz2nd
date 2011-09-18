# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from libwaz.contrib.calls import site
from libwaz.contrib.calls.backends import BasicCallsBackend

from models import Message

class MessageCallsBackend(BasicCallsBackend):
    MESSAGE = u"%(user_from)sさんからメッセージ「%(label)s」が届いています"
    
    def _post_save_callback(self, *args, **kwargs):
        pass
site.register(Message, MessageCallsBackend)