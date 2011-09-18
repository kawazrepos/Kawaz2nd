# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
class DuplicateError(Exception):
    pass

class DeletingFrozenTagError(Exception):
    u"""This exception occur when you tried to delete `frozen` tag"""
    pass
