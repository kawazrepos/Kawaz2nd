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

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.text import ugettext_lazy as _
from django.core.exceptions import ValidationError

from userel.fields import UserelField
from googlemap.models import GoogleMapField
from universaltag.fields import UniversalTagField

from kawaz.fields.contentfield.fields import ContentField

from utils import googlecalendar

class EventManager(models.Manager):
    """A Manager class of Event
    
    Attribute:
        active - return active events
        published - return published events
        draft - return draft events

    >>> manager = EventManager()
    >>> assert callable(getattr(manager, 'active'))
    >>> assert callable(getattr(manager, 'published'))
    >>> assert callable(getattr(manager, 'draft'))
    """
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


class Event(models.Model):
    """A Event model class
    
    Attribute:
        pub_state - publish state
        title - A title of the event
        body - A description of the event
        period_start - Start time of the event
        period_end - End time of the event
        place - A place of the event held
        location - Latitude, Longitude field for the event
        attendees - Attendees of the evetn
        author - Author of this event
        updated_by - Updater
        created_at - datetime created at
        updated_at - datetime updated at
        publish_at - datetime publish at
        publish_at_date - date publish at
        gcal_edit_link - Google Calender edit link (System)
        tags - ManyToMany relation to UniversalTag

    >>> event = Event()

    # Attributes event should have
    >>> assert hasattr(event, 'pub_state')
    >>> assert hasattr(event, 'title')
    >>> assert hasattr(event, 'body')
    >>> assert hasattr(event, 'period_start')
    >>> assert hasattr(event, 'period_end')
    >>> assert hasattr(event, 'place')
    >>> assert hasattr(event, 'location')
    >>> assert hasattr(event, 'created_at')
    >>> assert hasattr(event, 'updated_at')
    >>> assert hasattr(event, 'publish_at')
    >>> assert hasattr(event, 'publish_at_date')
    >>> assert hasattr(event, 'gcal_edit_link')

    # Automatically generated function via Django
    >>> assert callable(getattr(event, 'get_pub_state_display'))
    >>> assert callable(getattr(event, 'get_location_display'))

    # Required functions
    >>> assert callable(getattr(event, 'get_absolute_url'))
    >>> assert callable(getattr(event, 'attend'))
    >>> assert callable(getattr(event, 'leave'))
    >>> assert callable(getattr(event, 'is_active'))
    >>> assert callable(getattr(event, 'to_gcal_event'))
    """
    PUB_STATES = (
            ('public',  _('public')),
            ('protected', _('protected')),
            ('draft', _('draft'))
        )

    pub_state = models.CharField(_('publish state'), max_length=10,
                                 choices=PUB_STATES, default='public')
    title = models.CharField(_('title'), max_length=255)
    body = ContentField(_('description'))
    period_start = models.DateTimeField(_('start time'), blank=True, null=True)
    period_end = models.DateTimeField(_('end time'), blank=True, null=True)
    place = models.CharField(_('place'), max_length=255, blank=True)
    location = GoogleMapField(_('location'), blank=True, query_field_id='id_place')
    
    attendees = models.ManyToManyField(User, verbose_name=_('attendees'), 
                                       related_name='events_attend', null=True,
                                       editable=False, db_column='members')
    author = UserelField(_('author'), related_name='events_create', auto_now_add=True)
    updated_by = UserelField(_('updated_by'), related_name='events_update', auto_now=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    publish_at = models.DateTimeField(_('publish time'), null=True, editable=False)
    publish_at_date = models.DateField(_('publish date'), null=True, editable=False)
    
    gcal_edit_link = models.URLField(_('Google Calendar Edit Link'), db_column='gcal', null=True, editable=False)

    tags = UniversalTagField()

    objects = EventManager()
    
    class Meta:
        ordering = ('period_start', 'period_end', '-publish_at', '-updated_at', 'title')
        verbose_name = _('event')
        verbose_name_plural = _('events')
        permissions = (
                ('kick_event', 'Can kick a particular attendee'),
                ('attend_event', 'Can attend a particular event'),
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

    def is_active(self):
        """is this event over or not"""
        if not self.period_start:
            return True
        return self.period_end >= datetime.datetime.now()
    is_active.short_description = _('is this event over or not')
    is_active.boolean = True

    def to_gcal_event(self):
        """Create Google Calendar Event from this event"""
        kwargs = {
                'title': self.title,
                'content': self.body,
                'where': self.place,
            }
        if self.period_start and self.period_end:
            kwargs['when']= (
                    self.period_start, 
                    self.period_end,
                )
        gevent = googlecalendar.create_event(**kwargs)
        return gevent

#
# Google Calendar Sync
#
from django.db.models.signals import post_save, post_delete

def update_gcal_event_reciver(sender, instance, **kwargs):
    gevent = instance.to_gcal_event()

    if instance.pub_state != 'draft' and instance.period_start and instance.period_end:
        if instance.gcal_edit_link:
            # Update the event
            gevent = googlecalendar.update_event(instance.gcal_edit_link, gevent)
            if instance.gcal_edit_link != gevent.GetEditLink().href:
                instance.gcal_edit_link = gevent.GetEditLink().href
                instance.save()
        elif settings.GCAL_CALENDAR_ID:
            # Insert the event
            gevent = googlecalendar.insert_event(gevent)
            if gevent is None:
                return
            instance.gcal_edit_link = gevent.GetEditLink().href
            instance.save()
    elif instance.gcal_edit_link:
        # Remove the event
        googlecalendar.delete_event(instance.gcal_edit_link)
        instance.gcal_edit_link = None
        instance.save()

def delete_gcal_event_reciver(sender, instance, **kwargs):
    if instance.gcal_edit_link:
        googlecalendar.delete_event(instance.gcal_edit_link)
        instance.gcal_edit_link = None
    
post_save.connect(update_gcal_event_reciver, sender=Event)
post_delete.connect(delete_gcal_event_reciver, sender=Event)
