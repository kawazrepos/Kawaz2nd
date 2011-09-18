# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
class CallsError(Exception):
    """A generic exception for all others to extend."""
    pass
class AlreadyRegistered(CallsError):
    """Raised when a model is already registered with a site."""
    pass

class NotRegistered(CallsError):
    """Raised when a model is not registered with a site."""
    pass