# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/13
#
from django.shortcuts import render_to_response
from django.views.generic.list_detail import *

try:
    from libwaz.contrib.siever.views import object_filter
except ImportError:
    pass