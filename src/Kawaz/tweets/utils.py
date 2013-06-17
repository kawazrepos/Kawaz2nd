# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/01
#
from django.conf import settings
from django.utils import simplejson
from django.utils.html import strip_tags
from django.contrib.auth.models import User

from twitter.views import CONSUMER, CONNECTION
#from twitter.utils import update_status, get_user_timeline, SERVER
#from twitter.oauth import OAuthToken, OAuthConsumer

import tweepy
import httplib
import datetime
import calendar
import time
import warnings
import socket
import re

TWITTER_SOURCE = settings.TWITTER_SOURCE
TWITTER_HASHTAGS = settings.TWITTER_HASHTAGS
TWITTER_FOOTER = settings.TWITTER_HASHTAGS[0]
TWITTER_BODY_LENGTH_LIMIT = 140 - len(TWITTER_FOOTER) - 1

def _get_api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN=None, ACCESS_TOKEN_SECRET=None):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    if ACCESS_TOKEN and ACCESS_TOKEN_SECRET:
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

def twittertime2time(created_at):
    FORMAT = r'%a %b %d %H:%M:%S +0000 %Y'
    #
    # Notice:
    #    localeがC以外だと`strptime`が成功しないため
    #    localeをCに設定し`strptime`実行後にもとに戻す
    #
    import locale
    _tmp = locale.setlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, 'C')
    unix_time = calendar.timegm(time.strptime(created_at, FORMAT))
    locale.setlocale(locale.LC_ALL, _tmp)
    locale_time = time.localtime(unix_time)
    return datetime.datetime.fromtimestamp(time.mktime(locale_time))

def _to_twitter(value):
    u"""Kawaz用IDCallをTwitter用に書き換える"""
    PATTERN = r"@(?P<username>[a-zA-Z0-9_-]+)"
    def repl(m):
        username = m.group('username')
        try:
            profile = User.objects.get(username=username).get_profile()
            twitter = profile.services.filter(service='twitter', pub_state='public')
            if twitter.exists():
                return "@%s" % twitter[0].account
            else:
                return None
        except User.DoesNotExist:
            return None
    m = re.match(PATTERN, unicode(value))
    if not m:
        return value
    elif repl(m):
        return re.sub(PATTERN, repl, unicode(value))
    return None

def _from_twitter(value):
    u"""Twitter用IDCallをKawaz用に書き換える"""
    PATTERN = r"@(?P<account>[a-zA-Z0-9_-]+)"
    def repl(m):
        account = m.group('account')
        try:
            # 最初に可能な限り絞り込み
            users = User.objects.filter(is_active=True, profile__services__account=account)
            # 最終チェック
            for user in users:
                profile = user.get_profile()
                if profile.services.filter(pub_state='public', service='twitter', account=account).exists():
                    return "@%s" % profile.user.username
            # チェックが成功しなかった（Twitterじゃなかった or 公開範囲が内部限定）
            return account
        except User.DoesNotExist:
            return account
    value = re.sub(PATTERN, repl, unicode(value))
    return value

def post_twitter_with_bot(body, max_length=140):
    
    #
    # Note:
    #    Botは異なるCONSUMER_KEYを持っているため以下のように
    #    個別に行う必要がある
    #
    if not settings.TWITTER_ENABLE:
        return None
    HASHTAG = settings.TWITTER_HASHTAGS[0]
    
    CONSUMER_KEY = settings.BOT_CONSUMER_KEY
    CONSUMER_SECRET = settings.BOT_CONSUMER_SECRET
    ACCESS_TOKEN = settings.BOT_ACCESS_TOKEN
    ACCESS_TOKEN_SECRET = settings.BOT_ACCESS_TOKEN_SECRET
    
    status = u"%s %s" % (body, HASHTAG)
    api = _get_api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    try:
        # Post
        return api.update_status(status=status.encode('utf-8'))
    except socket.error, e:
        # TwitterはRequest Time Outになることがある
        warnings.warn(e.message)
        return None

def _parse_token(token):
    params = urlparse.parse_qs(s, keep_blank_values=False)
    key = params['oauth_token'][0]
    secret = params['oauth_token_secret'][0]
    return key, secret
    
def post_tweet_to_twitter(instance):
    u"""
    post tweets.tweet to twitter
    
    WARNING:
        DO NOT CALL this method while the instance is UPDATE
    """
    HASHTAG = settings.TWITTER_HASHTAGS[0]
    if not settings.TWITTER_ENABLE: return None
    if instance.source == 'twitter': return None
    token = instance.author.get_profile().twitter_token
    if not token: return None
    # Login
    key, secret = _parse_token(token)
    body = instance.body
    if len(body) > TWITTER_BODY_LENGTH_LIMIT:
        body = body[:TWITTER_BODY_LENGTH_LIMIT] + u"…"
    # @usernameが存在する場合はアカウントを検索
    #　存在しないreplyはTwitterに転送しない
    body = _to_twitter(body)
    if not body: return None
    status = u"%s %s" % (body, HASHTAG)
    #reply
    #投稿されたつぶやきが、replyであれば、reply先のつぶやきのtwitter_idを見て、
    #reply先もtwitter連携しているようであれば、in_reply_to_status_idを付加してAPIにPOSTする
    #(Kawaz内でのreply関係が、Twitter上でも反映されるようにする)
    in_reply_to = None
    if instance.reply and instance.reply.twitter_id:
        in_reply_to = instance.reply.twitter_id
    # Post
    try:
        tw = _get_api(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, key, secret)
        response = tw.update_status(status=status.encode("utf-8"), in_reply_to=in_reply_to)
        response = simplejson.loads(response)
        if 'error' in response:
            warnings.warn(response['error'])
            return None
        instance.twitter_id = response['id']
        instance.save()
    except socket.error, e:
        warnings.warn(e.message)
        return None
    return instance

def pull_tweet_from_twitter(user):
    # Notice: utilsはmodelsから読み込んでいるので以下を関数内にしないと無限ループ
    def include_hashtag(body):
        for hashtag in TWITTER_HASHTAGS:
            if hashtag in body: return hashtag
        return False
    from models import Tweet
    if not settings.TWITTER_ENABLE:
        return None
    token = user.get_profile().twitter_token
    if not token:
        return None
    # Login
    key, secret = _parse_token(token)
    # Get User Timeline
    tw = _get_api(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, key, secret)
    response = tw.user_timeline()
    timeline = simplejson.loads(response)
    if not timeline or isinstance(timeline, dict):
        warnings.warn("Could not pulled twitter timeline for %s: %s" % (user.username, timeline))
        return None
    tweets = []
    timeline.reverse()
    for tweet in timeline:
        twitter_id, source, body = tweet['id'], strip_tags(tweet['source']), tweet['text']
        created_at = twittertime2time(tweet['created_at'])
        footer = include_hashtag(body)
        if source == TWITTER_SOURCE or not footer:
            # Kawazから投稿されたTweetおよびハッシュタグを含まないものは破棄
            continue
        # 取得済みの場合は`twitter_id`が同一なのでチェック
        try:
            Tweet.objects.get(twitter_id=twitter_id)
            continue
        except Tweet.DoesNotExist:
            pass
        # 文末のハッシュタグを削除
        if body.endswith(footer):
            body = body[:-len(footer)]
        # Kawaz用にIDCallを書き換え
        body = _from_twitter(body)
        #reply
        #Twitter上のつぶやきがin_reply_to_status_id要素を持っていた場合、
        #それをtwitter_idに持っているTweetをデータベースから検索して、それにreplyするようなTweetを生成する
        try:
            in_reply_to_twitter_id = tweet['in_reply_to_status_id']
            in_reply_to = Tweet.objects.get(twitter_id=in_reply_to_twitter_id)
        except:
            in_reply_to = None
        # Create new tweet
        instance = Tweet.objects.create(
            author=user,
            twitter_id=twitter_id,
            body=body,
            source=u'twitter',
            created_at=created_at,
            reply=in_reply_to
        )
        tweets.append(instance)
    return tweets