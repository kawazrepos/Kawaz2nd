# -*- coding: utf-8 -*-
# Django settings for Kawaz project.
import sys
import os.path
ROOT = os.path.dirname(__file__)
PYTHON_PATHS = [
    os.path.abspath(os.path.join(ROOT, '../libs')),
]
for path in PYTHON_PATHS:
    if path not in sys.path: sys.path.append(path)

DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = (
    '127.0.0.1',
)

# 円周率は固定バージョン
# Ex:
#   0.3, 0.31, 0.314, 0.315, ...
VERSION = '0.31415rc4'

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(ROOT, "../../kawaz.db"),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for hlocalhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Tokyo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ja'
DATE_FORMAT = "Y年 m月d日(D)"
TIME_FORMAT = "H時i分"
DATETIME_FORMAT = "%s %s" % (DATE_FORMAT, TIME_FORMAT)
# Under apache/mod_wsgi LOCALE has to be set manually.
import locale
LOCALE = locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../../statics')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
# 以下値は setup_secret_key.sh にて自動的に書き換えられる
SECRET_KEY = ""

CACHE_BACKEND = 'locmem:///'

# List of callables that know how to import templates from various hsources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'Kawaz.profiles.middleware.RedirectIfProfileHasNotConfiguredMiddleware',
    'Kawaz.permissiongroups.middleware.PermissionGroupMiddleware',
    'libwaz.middleware.http.Http403Middleware',
    'libwaz.middleware.exception.UserBasedExceptionMiddleware',
    'libwaz.middleware.profile.ProfileMiddleware',
    'libwaz.contrib.calls.middleware.CallsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'Kawaz.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT, '../../templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.flatpages',
    'south',
    'compress',
    'haystack',
    'reversetag',
    'piston',
    'registration',
    'pagination',
    'libwaz.contrib.googlemap',
    'libwaz.contrib.evaluate',
    'libwaz.contrib.trackback',
    'libwaz.contrib.history',
    'libwaz.contrib.tagging',
    'libwaz.contrib.calls',
    'libwaz.contrib.drafts',
    'libwaz.contrib.object_permission',
    'libwaz.contrib.siever',
    # app
    'Kawaz.contact',
    'Kawaz.bugwaz',
    'Kawaz.defaultimg',
    'Kawaz.uni_form',
    'Kawaz.markitupfield',
    'Kawaz.templatetags',
    'Kawaz.threestep_registration',
    'Kawaz.permissiongroups',
    'Kawaz.profiles',
    'Kawaz.blogs',
    'Kawaz.events',
    'Kawaz.tweets',
    'Kawaz.commons',
    'Kawaz.projects',
    'Kawaz.mcomments',
    'Kawaz.threads',
    'Kawaz.wikis',
    'Kawaz.messages',
    'Kawaz.tasks',
    'Kawaz.announcements',
    'Kawaz.utilities',
)

FIXTURE_DIRS = (
    os.path.join(os.path.dirname(__file__), '../../fixtures'),
)
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: "/members/%s/" % o.username,
}

#
# PUB_STATES
#----------------------------------------------------------------------------
from django.utils.safestring import mark_safe
PUB_STATES = {
    'public':       ('public',      u"外部公開"),
    'protected':    ('protected',   u"内部公開"),
    'private':      ('private',     u"ヒミツ公開"),
    'group':        ('group',       u"グループ内公開"),
    'draft':        ('draft',       u"下書き"),
}
_pub_state_help_texts = {
    'public':       (u"外部公開",    u"外部ユーザにも公開します"),
    'protected':    (u"内部公開",    u"Kawazのメンバ全員に公開します"),
    'private':      (u"ヒミツ公開",  u"自分専用で公開します"),
    'group':        (u"グループ",    u"グループメンバのみに公開します"),
    'draft':        (u"下書き",      u"下書きとして保存します"),
}
def PUB_STATE_HELP_TEXT(pub_states):
    help_texts = []
    for pub_state in pub_states:
        help_text = u"<em>%s</em>: %s" % _pub_state_help_texts[pub_state[0]]
        help_texts.append(help_text)
    return mark_safe(u"<br />\n".join(help_texts))
#
# django.contrib.auth
#----------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'backends.auth.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
    'libwaz.contrib.object_permission.backends.ObjectPermBackend',
)
AUTH_PROFILE_MODULE = 'profiles.profile'
LOGIN_REDIRECT_URL  = "/"
LOGIN_URL = "/registration/login/"
LOGOUT_URL = "/registration/logout/"

ACCOUNT_ACTIVATION_DAYS = 7

#
# django.contrib.comments
#----------------------------------------------------------------------------
COMMENTS_APP = 'Kawaz.mcomments'
COMMENTS_HIDE_REMOVED = False

#
# libwaz.contrib.googlemap
#----------------------------------------------------------------------------
GOOGLEMAP_API_SENSOR = False
GOOGLEMAP_SCRIPT_URL = r'javascript/django/django.googlemap.js'

#
# django-markitupfield (tanix, alisue)
#----------------------------------------------------------------------------
import utils.markups
MARKUP_FIELD_TYPES = (
    ('markdown', utils.markups.markdown),
    ('comment_markdown', utils.markups.comment_markdown),
)

#
# django-compressed
#----------------------------------------------------------------------------
# 項目数があまりにも多いので全部インポートすることにした
import compress_settings
COMPRESS = not DEBUG
COMPRESS_CSS    = compress_settings.COMPRESS_CSS
COMPRESS_JS     = compress_settings.COMPRESS_JS

#
# django-haystack
#----------------------------------------------------------------------------
HAYSTACK_SITECONF = 'Kawaz.search_sites'
HAYSTACK_DEFAULT_OPERATOR = 'OR'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(ROOT, '../../whoosh')

#
# app.validator
#-----------------------------------------------------------------------------
VALIDATOR_INVALID_VALUES = (
    'central-dogma',
    'comments',
    'search',
    'trackback',
    'accounts',
    'history',
    'commons',
    'events',
    'tweets',
    'threads',
    'messages',
    'projects',
    'products',
    'stickies',
    'drafts',
    'announcements',
    'twitter',
    'tags',
    'create',
    'update',
    'delete',
    'feeds',
)

#
#Google Calendar
#-------------------------------------------------------------------------------
GCAL_LOGIN_EMAIL = "calendar@kawaz.org"
GCAL_LOGIN_PASS  = ""
#for DEBUG
GCAL_CALENDAR_ID = "kawaz.org_u41faouova38rcoh8eaimbg42c@group.calendar.google.com"

#
# tweets
#--------------------------------------------------------------------------------
CONSUMER_KEY            = ""
CONSUMER_SECRET         = ""
TWITTER_HASHTAGS        = (u"#Kawaz", u"#kawaz", )
TWITTER_SOURCE          = u'Kawaz'
BOT_CONSUMER_KEY        = ''
BOT_CONSUMER_SECRET     = ''
BOT_ACCESS_TOKEN        = ''
BOT_ACCESS_TOKEN_SECRET = ''
DEFAULT_TIMELINE_LENGTH = 6
TWITTER_ENABLE          = False

#
# Akismet
# added by giginet on 2011/7/20
#--------------------------------------------------------------------------------
TYPEPAD_ANTISPAM_API_KEY = ''
AKISMET_API_KEY = ''

#
# utilities.resave
#--------------------------------------------------------------------------------
RESAVE_WHITE_LIST = (
    'announcements.announcement',
    'blogs.entry',
    'profiles.profile',
    'events.event',
    'commons.material',
    'projects.project',
    'tasks.task',
    'mcomments.markitupcomment',
    'threads.thread',
    'wikis.entry',
)

def SYSTEM_USER():
    from django.contrib.auth.models import User
    return User.objects.get(username='system')

# 環境依存の設定（デプロイサーバー固有の設定など）を読み込む
try:
    from local_settings import *
except ImportError:
    pass
