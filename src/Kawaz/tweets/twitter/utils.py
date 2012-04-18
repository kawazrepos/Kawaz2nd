# -*- coding: utf-8 -*-
#
#    original http://github.com/henriklied/django-twitter-oauth
#    modified by giginet
#
import oauth
from django.conf import settings


signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

SERVER = getattr(settings, 'OAUTH_SERVER', 'twitter.com')
REQUEST_TOKEN_URL = getattr(settings, 'OAUTH_REQUEST_TOKEN_URL', 'https://%s/oauth/request_token' % SERVER)
ACCESS_TOKEN_URL = getattr(settings, 'OAUTH_ACCESS_TOKEN_URL', 'https://%s/oauth/access_token' % SERVER)
AUTHORIZATION_URL = getattr(settings, 'OAUTH_AUTHORIZATION_URL', 'http://%s/oauth/authorize' % SERVER)

CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY', 'YOUR_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET', 'YOUR_SECRET')

# We use this URL to check if Twitters oAuth worked
TWITTER_CHECK_AUTH = u'https://twitter.com/account/verify_credentials.json'
TWITTER_FRIENDS = u'https://twitter.com/statuses/friends.json'
TWITTER_UPDATE_STATUS = u'https://api.twitter.com/1/statuses/update.json'
TWITTER_USER_TIMELINE = u'https://api.twitter.com/1/statuses/user_timeline.json'

def request_oauth_resource(consumer, url, access_token, parameters=None, signature_method=signature_method, http_method="GET"):
    """
    usage: request_oauth_resource( consumer, '/url/', your_access_token, parameters=dict() )
    Returns a OAuthRequest object
    """
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, token=access_token, http_method=http_method, http_url=url, parameters=parameters,
    )
    oauth_request.sign_request(signature_method, consumer, access_token)
    return oauth_request


def fetch_response(oauth_request, connection):
    url = oauth_request.to_url()
    connection.request(oauth_request.http_method, url)
    response = connection.getresponse()
    s = response.read()
    return s

def get_unauthorised_request_token(consumer, connection, signature_method=signature_method):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, http_url=REQUEST_TOKEN_URL
    )
    oauth_request.sign_request(signature_method, consumer, None)
    resp = fetch_response(oauth_request, connection)
    token = oauth.OAuthToken.from_string(resp)
    return token


def get_authorisation_url(consumer, token, signature_method=signature_method):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, token=token, http_url=AUTHORIZATION_URL
    )
    oauth_request.sign_request(signature_method, consumer, token)
    return oauth_request.to_url()

def exchange_request_token_for_access_token(consumer, connection, request_token, signature_method=signature_method):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, token=request_token, http_url=ACCESS_TOKEN_URL
    )
    oauth_request.sign_request(signature_method, consumer, request_token)
    resp = fetch_response(oauth_request, connection)
    return oauth.OAuthToken.from_string(resp) 

def is_authenticated(consumer, connection, access_token):
    oauth_request = request_oauth_resource(consumer, TWITTER_CHECK_AUTH, access_token)
    json = fetch_response(oauth_request, connection)
    if 'screen_name' in json:
        return json
    return False

def get_friends(consumer, connection, access_token, page=0):
    """Get friends on Twitter"""
    oauth_request = request_oauth_resource(consumer, TWITTER_FRIENDS, access_token, {'page': page})
    json = fetch_response(oauth_request, connection)
    return json

#
#    つぶやきにin_reply_toが付加できるように拡張 by giginet
#
def update_status(consumer, connection, access_token, status, in_reply_to=None):
    """Update twitter status, i.e., post a tweet"""
    oauth_request = request_oauth_resource(consumer,
                                           TWITTER_UPDATE_STATUS,
                                           access_token,
                                           {'status': status,
                                            'in_reply_to_status_id': in_reply_to},
                                           http_method='POST')
    json = fetch_response(oauth_request, connection)
    return json

def get_user_timeline(consumer, connection, access_token):
    """Get UserTimeline on Twitter."""
    oauth_request = request_oauth_resource(consumer,
                                           TWITTER_USER_TIMELINE,
                                           access_token,
                                           http_method='GET')
    json = fetch_response(oauth_request, connection)
    return json

def shorten(url):
    from urllib2 import urlopen, Request, HTTPError
    from django.utils.simplejson import loads, dumps
    API_URL = 'https://www.googleapis.com/urlshortener/v1/url'
    try:
        data = dumps({ 'longUrl' : url })
        req = Request(API_URL, data)
        req.add_header('Content-Type', 'application/json')
        r = urlopen(req)
        return loads(r.read())['id']
    except HTTPError:
        return url

