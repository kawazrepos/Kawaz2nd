# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from libwaz.contrib.calls import site
from libwaz.contrib.calls.backends import IdCallsBackend

from models import Tweet

site.register(Tweet, IdCallsBackend)