# vim: set fileencoding=utf8:
"""
short module explanation

AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
__VERSION__ = "0.1.0"

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('alisue',      'lambdalisue+kawaz@hashnote.net'),
    ('giginet',     'giginet.net+kawaz@gmail.com'),
)
MANAGERS = ADMINS

# Use deploy database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'webmaster@kawaz.org'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
DEFAULT_EMAIL = 'webmaster@kawaz.org'
DEFAULT_FROM_EMAIL = DEFAULT_EMAIL

# -- Google Calendar
GCAL_LOGIN_PASS  = ""
GCAL_CALENDAR_ID = "kawaz.org_knp8k16jovqbodorkrkt45un0o@group.calendar.google.com"

# -- Twitter
CONSUMER_KEY            = ''
CONSUMER_SECRET         = ''
BOT_CONSUMER_KEY        = ''
BOT_CONSUMER_SECRET     = ''
BOT_ACCESS_TOKEN        = ''
BOT_ACCESS_TOKEN_SECRET = ''
TWITTER_ENABLE          = True

# -- haystack
HAYSTACK_SEARCH_ENGINE = "solr"
HAYSTACK_SOLR_URL = "http://localhost:8983/solr"

# -- akismet
TYPEPAD_ANTISPAM_API_KEY = ''
AKISMET_API_KEY = ''

LOCAL_SETTINGS_LOADED = True
