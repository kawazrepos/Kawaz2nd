# -*- coding: utf-8 -*-
#
# Created:    2010/11/07
# Author:         alisue
#
from models import Call
from urllib import quote

class CallsMiddleware(object):
    u"""
    make `read` to True for the particular url call
    """
    def process_request(self, request):
        if request.user.is_authenticated():
            try:
                url = quote(request.path.encode('utf-8'))
                call = Call.objects.get(url=url, user_to=request.user)
                call.read = True
                call.save()
            except Call.DoesNotExist:
                pass
#            except:
#                # Fail silently
#                pass
        return None