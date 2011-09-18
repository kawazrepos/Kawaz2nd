# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/29
#
from django.dispatch import Signal

pre_save = Signal(providing_args=["instance", "request"])
post_save = Signal(providing_args=["instance", "created", "request"])
pre_delete = Signal(providing_args=["instance", "request"])
post_delete = Signal(providing_args=["instance", "request"])