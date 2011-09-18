# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/01
#
from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import DjangoAuthentication

from handlers import TweetHandler

tweet_handler = Resource(TweetHandler, authentication=DjangoAuthentication())

urlpatterns = patterns('',
   url(r'^(?P<object_id>\d+)/$',   tweet_handler,  name="tweets-tweet-api-tweet"),
   url(r'^$',                      tweet_handler,  name="tweets-tweet-api-tweet"),
)
