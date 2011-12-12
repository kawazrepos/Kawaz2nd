#!/usr/bin/env python
# vim: set fileencoding=utf8 :
"""Local settings module

This module never shared via Github. So use this module
to configure secret data like Password or whatever.


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
__author__  = 'Alisue <lambdalisue@hashnote.net>'
__version__ = '1.0.0'
__date__    = '2011/06/09'
import sys
import os.path
ROOT = os.path.join(os.path.dirname(__file__), '../../')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.sqlite3',   # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME':     os.path.join(ROOT, 'sqlite3.db'), # Or path to database file if using sqlite3.
        'USER':     '',                             # Not used with sqlite3.
        'PASSWORD': '',                             # Not used with sqlite3.
        'HOST':     '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT':     '',                             # Set to empty string for default. Not used with sqlite3.
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = "Make this unique, and don't share it with anybody."

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Mark that local_settings has loaded correctly
LOCAL_SETTINGS_LOADED = True
