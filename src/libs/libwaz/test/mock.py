# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/12
#
from django.test import Client
from django.core.handlers.wsgi import WSGIRequest

__all__ = ['MockRequestClient', 'mock_request']

class MockRequestClient(Client):
    """
    A ``django.test.Client`` subclass which can return mock
    ``HttpRequest`` objects.
    
    """
    def request(self, **request):
        """
        Rather than issuing a request and returning the response, this
        simply constructs an ``HttpRequest`` object and returns it.
        
        """
        environ = {
            'HTTP_COOKIE':      self.cookies,
            'PATH_INFO':         '/',
            'QUERY_STRING':      '',
            'REMOTE_ADDR':       '127.0.0.1',
            'REQUEST_METHOD':    'GET',
            'SCRIPT_NAME':       '',
            'SERVER_NAME':       'testserver',
            'SERVER_PORT':       '80',
            'SERVER_PROTOCOL':   'HTTP/1.1',
            'wsgi.version':      (1,0),
            'wsgi.url_scheme':   'http',
            'wsgi.errors':       self.errors,
            'wsgi.multiprocess': True,
            'wsgi.multithread':  False,
            'wsgi.run_once':     False,
            }
        environ.update(self.defaults)
        environ.update(request)
        return WSGIRequest(environ)


def mock_request():
    """
    Construct and return a mock ``HttpRequest`` object; this is used
    in testing backend methods which expect an ``HttpRequest`` but
    which are not being called from views.
    
    """
    return MockRequestClient().request()