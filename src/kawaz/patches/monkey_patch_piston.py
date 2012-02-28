#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
Monkey patch for django-piston 0.2.3

1.  Download missing fixture and save to ``fixtures`` directory
2.  Add some missing attribute to HttpResponse (insted of HttpResponseWrapper
    which is not be able to access)


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
License:
    The MIT License (MIT)

    Copyright (c) 2012 Alisue allright reserved.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.

"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
import os
import urllib
import logging

import piston

logger = logging.getLogger(__name__)

# does fixture exists? piston 0.2.3 doesn't contain fixture data
fixture_url = "https://bitbucket.org/jespern/django-piston/raw/4fe8af1db59d/piston/fixtures/models.json"
fixture_path = os.path.join(piston.__path__[0], 'fixtures', 'models.json') 
if not os.path.exists(fixture_path):
    logger.info("fixtures for piston 0.2.3 is not found.")
    dirname = os.path.dirname(fixture_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    logger.info("downloading fixtures from '%s'" % fixture_url)
    # download fixture from web
    urllib.urlretrieve(fixture_url, fixture_path)
    logger.info("fixture was correctly installed.")

# support Django 1.4 monkey patch
from django.http import HttpResponse
def _get__is_string(self):
    return self.__is_string
def _set__is_string(self, value):
    self.__is_string = value
    self._base_content_is_iter = not value
HttpResponse.__is_string = 'Expected response content to be a string'
HttpResponse._is_string = property(_get__is_string, _set__is_string)
HttpResponse._base_content_is_iter = True

