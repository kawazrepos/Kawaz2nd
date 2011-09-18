# -*- coding: utf-8 -*-
#
# Created:        2010/11/08
# Author:        alisue
#
from registration.signals import *


# A new user has approved.
user_approved = Signal(providing_args=["user", "request"])

# A user has rejected his or her account.
user_rejected = Signal(providing_args=["user", "request"])

user_withdrawed = Signal(providing_args=["user", "request"])