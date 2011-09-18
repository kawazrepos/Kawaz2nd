# -*- coding: utf-8 -*-
#
# Created:    2010/10/10
# Author:         alisue
#
from django.contrib.syndication.views import Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
lazy_reverse = lazy(reverse, str)

from models import Tweet

class LatestTweetFeed(Feed):
    title       = u"かわずったーのタイムライン更新情報 - Kawaz.tk"
    description = u"札幌ゲーム製作者コミュニティKawazのかわずったーの更新情報"
    link        = lazy_reverse('tweets-tweet-feeds')
    
    def items(self):
        queryset = Tweet.objects.all()
        return queryset[:50]
    
    def item_title(self, item):
        return u"%sさんのつぶやき" % item.author.get_profile().nickname
    
    def item_description(self, item):
        return item.body
    
    def item_link(self, item):
        return item.get_absolute_url()

class IndividualTweetFeed(Feed):
    title       = u"かわずったーのタイムライン更新情報 - Kawaz.tk"
    description = u"札幌ゲーム製作者コミュニティKawazのかわずったーの更新情報"
    link        = lazy_reverse('tweets-tweet-feeds-individual')
    
    def get_object(self, bits):
        # In case of "/rss/beats/0613/foo/bar/baz/", or other such clutter,
        # check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return bits[0]

    def title(self, obj):
        return u"%sさんのかわずったータイムライン - Kawaz.tk" % obj.get_profile().nickname

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return reverse('tweets-tweet-feeds-individual', (), {'user_id': obj.pk})

    def description(self, obj):
        return u"%sさんのつぶやき更新情報" % obj.get_profile().nickname

    def items(self, obj):
        queryset = Tweet.objects.filter(author=obj)
        return queryset[:50]
    
    def item_title(self, item):
        return u"%sさんのつぶやき" % item.author.get_profile().nickname
    
    def item_description(self, item):
        return item.body
    
    def item_link(self, item):
        return item.get_absolute_url()
