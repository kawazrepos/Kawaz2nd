# -*- coding: utf-8 -*-
#
# Created:    2010/10/09
# Author:         alisue
#
from django.contrib.sites.models import Site

import urllib
import urlparse
import httplib
import re

class Trackback(object):
    u"""Trackback class"""
    def __init__(self, url, title='', excerpt='', blog_name=''):
        self.url = url
        self.title = title if title else self.url
        self.excerpt = excerpt
        self.blog_name = blog_name
        if self.url.startswith('/'):
            # To absolute url
            self.url = "http://%s%s" % (
                Site.objects.get_current().domain,
                self.url
            )
    def ping(self, url):
        u"""Ping to the trackback ping url"""
        if not url: 
            return None
        params = urllib.urlencode(dict([k, v.encode('utf-8') if isinstance(v, unicode) else v] for k, v in {
            'url':          self.url,
            'title':        self.title,
            'excerpt':      self.excerpt,
            'blog_name':    self.blog_name
        }.items()))
        headers = {
            'Content-type': "application/x-www-form-urlencoded",
        }
        host, path = urlparse.urlparse(url)[1:3]
        connection = httplib.HTTPConnection(host)
        connection.request("POST", path, params, headers)
        response = connection.getresponse()
        connection.close()
        return response
    
    @staticmethod
    def autodiscover(url):
        u"""Connect to the url and find `trackback ping meta info` from the page."""
        host, path = urlparse.urlparse(url)[1:3]
        connection = httplib.HTTPConnection(host)
        connection.request("GET", path)
        response = connection.getresponse()
        buffer = response.read()
        pattern = r'trackback:ping="(.*?)"'
        r = re.search(pattern, buffer)
        if r: return r.group(1)
        return None
    
    @staticmethod
    def findurls(text):
        u"""Find all url patterns in the text."""
        pattern = r'http://[^\s]+'
        r = re.findall(pattern, text)
        return r