"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test.client import Client
from nose.tools import *

class TestThumbnailField(object):
    def test_thumbnail_generate(self):
        """
            Tests thumbnail generating
        """
