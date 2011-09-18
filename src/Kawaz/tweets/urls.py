# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views
import twitter.urls

extra_patterns = patterns('',
    url(r'^$',                              views.tweet_list,           name='tweets-tweet-list'),
    url(r'^(?P<object_id>\d+)/$',           views.tweet_detail,         name='tweets-tweet-detail'),
    url(r'^favorites/$',                    views.tweet_favorite_list,  name='tweets-tweet-favorite-list'),
)
urlpatterns = patterns('',
    url(r'^$',                              views.tweet_list,           name='tweets-tweet-list'),
    url(r'^create/$',                       views.create_tweet,         name='tweets-tweet-create'),
    url(r'^(?P<object_id>\d+)/delete/$',    views.delete_tweet,         name='tweets-tweet-delete'),
    url(r'^favorite/$',                     views.favorite_tweet,       name='tweets-tweet-favorite'),
    url(r'^favorites/$',                    views.tweet_favorite_list,  name='tweets-tweet-favorite-list'),
    (r'^twitter/',                          include(twitter.urls)),
    (r'^(?P<author>[^/]+)/',                include(extra_patterns))
)
from feeds import LatestTweetFeed, IndividualTweetFeed
urlpatterns += patterns('',
    (r'^feeds/$',   LatestTweetFeed(),      {}, 'tweets-tweet-feeds'),
    (r'^feeds/(?P<author>[^/]+)/$',   IndividualTweetFeed,    {}, 'tweets-tweet-feeds-individual'),
)
