# vim: set fileencoding=utf8:
"""
Kawaz Profile models

CLASS:
    Skill - A skill
    ProfileManager - A profile manager
    Profile - A profile
    Service - A service


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
import os
import warnings

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.text import ugettext_lazy as _

from universaltag.fields import UniversalTagField
from googlemap.models import GoogleMapField
from thumbnailfield.models import ThumbnailField
from object_permission import ObjectPermissionMediator

from kawaz.utils.default.image import get_default_profile_icon


class Skill(models.Model):
    """Skill of each profile
    
    Attribute:
        label - A label of the skill
        order - An integer value for ordering skill

    >>> skill = Skill()
    >>> assert hasattr(skill, 'label')
    >>> assert hasattr(skill, 'order')
    """
    label = models.CharField(_('skill'), unique=True, max_length=32)
    # TODO: should use `Meta.order_with_respect_to`
    order = models.IntegerField(_('order'), default=0)

    def __unicode__(self):
        return self.label

    class Meta:
        ordering = ['order']
        verbose_name = _('skill')
        verbose_name_plural = _('skills')


class ProfileManager(models.Manager):
    """Manager class of profile
    
    Attribute:
        published - get published profile queryset

    >>> manager = ProfileManager()
    >>> assert hasattr(manager, 'published')
    """
    def published(self, request):
        """get published profile queryset
        
        exclude profile which hasn't set nickname yet and exclude profile
        which user is inactive.

        return queryset of ``pub_state='public'`` profile only for anonymous
        user.
        """
        qs = self.exclude(nickname=None).exclude(user__is_active=False)
        if request and request.user.is_authenticated():
            return qs
        else:
            return qs.filter(pub_state='public')
        

class Profile(models.Model):
    """Profile of each user
    
    Attribute:
        pub_state - publish state
        nickname - A nickname of user. User must set nickname
        mood - A mood string
        icon - An avatar of user
        sex - sex of user
        birthday - birthday of user
        place - place user live
        location - Geometry data of ``place``
        url - URL
        remarks - An text field
        skills - ManyToMany relation to Skill
        user - OneToOne relation to User
        twitter_token - set if user authenticate twitter
        created_at - datetime created at
        updated_at - datetime updated at
        tags - ManyToMany relation to UniversalTag

        modify_object_permission - set object permission of this
        get_absolute_url - get absolute permalink of this
        get_icon_display - get ``img`` tag for displaying avatar
        get_nickname_display - get ``a`` tag for displaying nickname

        is_authenticated_twitter - for django-admin site

    >>> profile = Profile()

    # Attributes profile should have
    >>> assert hasattr(profile, 'pub_state')
    >>> assert hasattr(profile, 'nickname')
    >>> assert hasattr(profile, 'mood')
    >>> assert hasattr(profile, 'icon')
    >>> assert hasattr(profile, 'sex')
    >>> assert hasattr(profile, 'birthday')
    >>> assert hasattr(profile, 'place')
    >>> assert hasattr(profile, 'location')
    >>> assert hasattr(profile, 'url')
    >>> assert hasattr(profile, 'remarks')
    >>> assert hasattr(profile, 'twitter_token')
    >>> assert hasattr(profile, 'created_at')
    >>> assert hasattr(profile, 'updated_at')
    >>> assert hasattr(profile, 'tags')

    # Automatically generated function via Django
    >>> assert callable(getattr(profile, 'get_pub_state_display'))
    >>> assert callable(getattr(profile, 'get_sex_display'))

    # Required functions
    >>> assert callable(getattr(profile, 'get_absolute_url'))
    >>> assert callable(getattr(profile, 'get_huge_avatar_display'))
    >>> assert callable(getattr(profile, 'get_large_avatar_display'))
    >>> assert callable(getattr(profile, 'get_middle_avatar_display'))
    >>> assert callable(getattr(profile, 'get_small_avatar_display'))
    >>> assert callable(getattr(profile, 'get_nickname_display'))

    # Automatically called required functions
    >>> assert callable(getattr(profile, 'modify_object_permission'))
    >>> assert callable(getattr(profile, 'is_authenticated_twitter'))
    """
    def _get_upload_path(self, filename):
        basepath = u"storage/profiles/%s" % self.user.username
        return os.path.join(basepath, filename)

    PUB_STATES = (
            ('public',      _('public')),
            ('protected',   _('protected')),
        )
    SEX_TYPES = (
            ('man',         _('man')),
            ('woman',       _('woman')),
        )
    THUMBNAIL_SIZE_PATTERNS = {
            'huge': (288, 288, False),
            'large': (96, 96, False),
            'middle': (48, 48, False),
            'small': (24, 24, False),
        }

    pub_state = models.CharField(_('publish state'), max_length=10, 
                                 choices=PUB_STATES, default='public')
    # Note: To check the user update profile or not, nickname can be null
    # in DB level.
    nickname = models.CharField(_('nickname'), max_length=30, unique=True,
                                blank=False, null=True)

    mood = models.CharField(_('mood'), max_length=127, blank=True)
    # TODO: ``avatar`` is the better name for this field.
    icon = ThumbnailField(_('avatar'), upload_to=_get_upload_path, blank=True,
                          thumbnail_size_patterns=THUMBNAIL_SIZE_PATTERNS)
    sex = models.CharField(_('sex'), max_length=10, choices=SEX_TYPES,
                           blank=True)
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    # TODO: ``address` is the better name for this field.
    place = models.CharField(
            _('address'), max_length=255, blank=True,
            help_text=_('the address is not shown for anonymous user'))
    location = GoogleMapField(_('location'), blank=True,
                              query_field_id='id_place')

    url = models.URLField(_('url'), max_length=255, blank=True)
    remarks = models.TextField(_('remarks'), blank=True)
    skills = models.ManyToManyField(Skill, verbose_name=_('skill'),
                                    related_name='users', null=True, blank=True)

    user = models.ForeignKey(User, verbose_name=_('account'),
                             related_name='profile', unique=True,
                             primary_key=True, editable=False)
    twitter_token = models.CharField(_('twitter oauth access token'),
                                     max_length=1023, editable=False,
                                     blank=True)
    created_at = models.DateTimeField(_('date time created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date time updated'), auto_now=True)

    tags = UniversalTagField()

    objects = ProfileManager()

    class Meta:
        ordering = ('-user__last_login', 'nickname')
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __unicode__(self):
        if self.nickname:
            return self.nickname
        return _('non active user (%s)') % self.user.username

    def modify_object_permission(self, mediator, created):
        mediator.manager(self, self.user)
        if self.pub_state == 'public':
            mediator.viewer(self, None)
            mediator.viewer(self, 'anonymous')
        else:
            mediator.viewer(self, None)
            mediator.reject(self, 'anonymous')

    @models.permalink
    def get_absolute_url(self):
        """get absolute permalink of this profile"""
        return ('profiles-profile-detail', (), {'slug': self.user.username})

    # deprecated at 0.314159 ---
    def get_icon_display(self, pattern_name):
        warnings.warn('deprecated. use get_XXX_avatar_display insted', DeprecationWarning)
        return self._get_avatar_display(self, pattern_name)
    get_icon_huge_display = lambda self: self.get_icon_display('huge')
    get_icon_large_display = lambda self: self.get_icon_display('large')
    get_icon_middle_display = lambda self: self.get_icon_display('middle')
    get_icon_small_display = lambda self: self.get_icon_display('small')
    # --------------------------
    def _get_avatar_display(self, pattern_name):
        """get ``img`` tag safe string of ``icon`` field for displaying"""
        kwargs = {
                'alt': _('avatar of %s') % self.nickname,
                'title': _('%(nickname)s [%(mood)s]') % {
                    'nickname': self.nickname,
                    'mood': self.mood
                },
            }
        if self.icon:
            kwargs['src'] = getattr(self.icon, pattern_name).url
        else:
            kwargs['src'] = get_default_profile_icon(pattern_name, self.pk)
        pattern = r"""<img src='%(src)s' alt='%(alt)s' title='%(title)s' />"""
        return mark_safe(pattern % kwargs)
    get_huge_avatar_display = lambda self: self._get_avatar_display('huge')
    get_large_avatar_display = lambda self: self._get_avatar_display('large')
    get_middle_avatar_display = lambda self: self._get_avatar_display('middle')
    get_small_avatar_display = lambda self: self._get_avatar_display('small')

    def get_nickname_display(self):
        """get ``a`` tag safe string of ``nickname`` field for displaying"""
        kwargs = {
                'href': self.get_absolute_url(),
                'title': _('@%(username)s') % {'username': self.user.username},
                'nickname': self.nickname,
            }
        pattern = r"""<a href='%(href)s' title='%(title)s'>%(nickname)s</a>"""
        return mark_safe(pattern % kwargs)

    # Admin
    def is_authenticated_twitter(self):
        """get the user has authenticated twitter or not"""
        return bool(self.twitter_token)
    is_authenticated_twitter.short_description = _('Connected with Twitter')
    is_authenticated_twitter.boolean = True

            
class Service(models.Model):
    """Service user use
    
    Attribute:
        pub_state - publish state
        profile - OneToOne relation to profile
        service - service name
        account - service account

    >>> service = Service()

    # Attributes service should have
    >>> assert hasattr(service, 'pub_state')
    >>> assert hasattr(service, 'service')
    >>> assert hasattr(service, 'account')

    # Automatically generated function via Django
    >>> assert callable(getattr(service, 'get_pub_state_display'))
    >>> assert callable(getattr(service, 'get_service_display'))

    # Required functions
    >>> assert callable(getattr(service, 'get_account_display'))
    >>> assert callable(getattr(service, 'get_service_icon_display'))

    """
    PUB_STATES = (
            ('public', _('public')),
            ('protected', _('protected')),
        )
    SERVICES = (                                                    
            ('skype', _('Skype')),
            ('wlm', _('Windows Live Messenger')),
            ('twitter', _('Twitter')),
            ('mixi', _('Mixi')),
            ('facebook', _('Facebook')),
            ('foursquare', _('foursquare')),
            ('google', _('Google')),
            ('pixiv', _('Pixiv')),
            ('hatena', _('Hatena')),
            ('xbl', _('Xbox Live')),
            ('psn', _('PlayStation Network')),
            ('dropbox', _('Dropbox')),
        )
    profile = models.ForeignKey(Profile, verbose_name=_('profile'), 
                                related_name=_('services'), editable=False)
    pub_state = models.CharField(_('publish state'), max_length=10,
                                 choices=PUB_STATES, default='public')
    service = models.CharField(_('service name'), max_length=20,
                               choices=SERVICES)
    account = models.CharField(_('service account'), max_length=127)

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
        # Nobody have same account on same service
        unique_together = ('service', 'account')

    def __unicode__(self):
        return "%s - [%s]" % (self.account, self.service)

    def get_account_display(self):
        """get ``a`` tag safe string of ``account`` for displaying"""
        SERVICE_LINKS = {
            "skype": u"skype:%s?add",
            "wlm": u"mailto:%s",
            "twitter": u"http://twitter.com/%s/",
            "mixi": u"http://mixi.jp/show_profile.pl?id=%s",
            "facebook": u"http://www.facebook.com/%s",
            'foursquare': u"http://foursquare.com/%s",
            "google": u"mailto:%s@gmail.com",
            "pixiv": u"http://www.pixiv.net/member.php?id=%s",
            "hatena": u"http://d.hatena.ne.jp/%s/",
            "xbl": u"http://live.xbox.com/ja-JP/MyXbox/Profile?gamertag=%s",
            "psn": u"http://playstationhome.jp/community/mypage.php?OnlineID=%s",
            "dropbox": u"mailto:%s",
        }
        kwargs = {
                'href': SERVICE_LINKS[self.service],
                'label': self.account
            }
        pattern = r"""<a href='%(href)s' target='_blank'>%(label)s</a>"""
        return mark_safe(pattern % kwargs)
        
    def get_service_icon_display(self):
        """get ``img`` tag safe string of ``service`` for displaying"""
        kwargs = {
                'alt': self.get_service_display(),
                'title': self.get_sertice_display(),
            }
        pattern = r"""%(MEDIA_ROOT)simage/serviceicons/%(name)s.png"""
        kwargs['src'] = pattern % {
                'MEDIA_ROOT': settings.MEDIA_ROOT,
                'name': self.service,
            }
        pattern = r"""<img src='%(src)s' alt='%(alt)s' title='%(title)s'>"""
        return mark_safe(pattern % kwargs)

from django.db.models.signals import post_save
def create_profile(sender, instance, created, **kwargs):
    """automatically create profile when user instance created"""
    if not created: return
    new = Profile(user=instance)
    new.save()
    # set object permissions
    ObjectPermissionMediator.manager(new, instance)
post_save.connect(create_profile, sender=User)
