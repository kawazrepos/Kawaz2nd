# vim: set fileencoding=utf8:
"""
Model class of Kawaz Event System


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
import datetime

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.text import ugettext_lazy as _
from django.core.exceptions import ValidationError

from author.decorators import with_author
from googlemap.models import GoogleMapField
from universaltag.fields import UniversalTagField

from kawaz.utils.decorators import with_datetime
from kawaz.fields.contentfield.fields import ContentField

class EventManager(models.Manager):
    """A Manager class of Event"""
    def active(self, request):
        """return active events"""
        qs = self.published(request)
        qs = qs.filter(Q(period_end__gte=datetime.datetime.now()) | Q(period_end=None)).distinct()
        return qs
    
    def published(self, request):
        """return published events"""
        q = Q(pub_state='public')
        if request.user.has_perm('events.view_protected_event'):
            q |= Q(pub_state='protected')
        return self.filter(q).distinct()

    def draft(self, request):
        """return draft events"""
        if request.user.is_authenticated():
            return self.filter(author=request.user, pub_state='draft')
        else:
            return self.none()


@with_author
@with_datetime
class Event(models.Model):
    """A Event model class"""
    PUB_STATES = (
            ('public',  _('public')),
            ('protected', _('protected')),
            ('draft', _('draft'))
        )
    pub_state = models.CharField(_('publish state'), max_length=10,
                                 choices=PUB_STATES, default='public')
    title = models.CharField(_('title'), max_length=255)
    # body -> description
    description = ContentField(_('description'))
    period_start = models.DateTimeField(_('start time'), blank=True, null=True)
    period_end = models.DateTimeField(_('end time'), blank=True, null=True)
    place = models.CharField(_('place'), max_length=255, blank=True)
    location = GoogleMapField(_('location'), blank=True, query_field_id='id_place')
    
    attendees = models.ManyToManyField(User, verbose_name=_('attendees'), 
                                       related_name='events_attend', null=True,
                                       editable=False)
    publish_at = models.DateTimeField(_('publish time'), null=True, editable=False)
    publish_at_date = models.DateField(_('publish date'), null=True, editable=False)

    gcal = models.URLField('GCalEditLink', blank=True, null=True, editable=False)
    tags = UniversalTagField()

    objects = EventManager()
    
    class Meta:
        ordering = ('period_start', 'period_end', '-publish_at', '-updated_at', 'title')
        verbose_name = _('event')
        verbose_name_plural = _('events')
        permissions = (
                ('kick_event', 'Can kick a particular attendee'),
                ('attend_event', 'Can attend a particular event'),
                ('view_protected_event', 'Can view a protected event'),
            )

    def __unicode__(self):
        return self.title

    def clean(self):
        if self.pub_state == 'draft' and self.publish_at:
            # draft event should not have publish_at
            self.publish_at = None
            self.publish_at_date = None
        elif self.pub_state != 'draft' and not self.publish_at:
            # published event should have publish_at
            self.publish_at = datetime.datetime.now()
            self.publish_at_date = datetime.datetime.now()
        if not self.place and self.location:
            raise ValidationError(_('You cannot set the location while the place is not filled.'
                                    ' Please fill the place or hide the map.'))
        if self.period_start and self.period_end:
            if self.period_start > self.period_end:
                # As time goes by.
                raise ValidationError(_('The time goes forward, not backward ;-)'))
            elif self.period_start < datetime.datetime.now():
                # Is this new ?
                created = self.pk or not Event.objects.filter(pk=self.pk).exists()
                if created:
                    # Dr. Emmett - Google 'Back to the future'
                    raise ValidationError(_('Nobody can attend the event without Dr. Emmett :-('))
            elif (self.period_end - self.period_start).days > 7:
                # God creats the world in 7 days.
                raise ValidationError(_('Are you going to create the world? The event should not be longer than 7 days.'))
        elif self.period_end:
            raise ValidationError(_('You cannot finish the work while you have not started.'))

    def attend(self, user):
        """Attend the event"""
        self.attendees.add(user)

    def leave(self, user):
        """Leave the event"""
        if user == self.author:
            raise AttributeError(_('Author cannot leave the event.'))
        self.attendees.remove(user)

    @models.permalink
    def get_absolute_url(self):
        if self.pub_state == 'draft':
            return ('events-event-update', (), {'pk': self.pk})
        return ('events-event-detail', (), {'pk': self.pk})

    def get_place_display(self):
        """return HTML code with map"""
        if self.place:
            return mark_safe('''<p>%s</p>%s'''%(self.place, self.get_location_display))
        else:
            return _('---')
    get_place_display.short_description = _('A place of the event')

    def is_active(self):
        """is this event end or not"""
        if not self.period_start:
            return True
        return self.period_end >= datetime.datetime.now()
    is_active.short_description = _('is this event end or not')
    is_active.boolean = True

