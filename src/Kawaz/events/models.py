# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError

from ..markitupfield.models import MarkItUpField

from libwaz.db import models
from libwaz.db.models import Q
from libwaz.utils.humanize import humanize_datetime, humanize_relativedelta
from libwaz.contrib.tagging.fields import TaggingField
from libwaz.contrib.googlemap.models import GoogleMapField
from libwaz.contrib.history import site

import datetime
from dateutil.relativedelta import relativedelta

class EventManager(models.Manager):
    def active(self, request):
        qs = self.published(request)
        qs = qs.filter(Q(period_end__gte=datetime.datetime.now()) | Q(period_end=None)).distinct()
        return qs
    
    def published(self, request):
        q = Q(pub_state='public')
        if request and request.user.is_authenticated():
            q |= Q(pub_state='protected')
        return self.filter(q).distinct()
    
    def draft(self, request):
        if request and request.user.is_authenticated():
            return self.filter(author=request.user, pub_state='draft')
        else:
            return self.none()

class Event(models.ModelWithRequest):
    u"""イベント詳細のモデル"""
    PUB_STATES = (
        settings.PUB_STATES['public'],
        settings.PUB_STATES['protected'],
        settings.PUB_STATES['draft']
    )
    # Required
    pub_state       = models.CharField(u"公開設定", max_length=10, choices=PUB_STATES, default="public", help_text=settings.PUB_STATE_HELP_TEXT(PUB_STATES))
    title           = models.CharField(u"イベント名", max_length=255)
    body            = MarkItUpField(u"イベント詳細", default_markup_type="markdown")
    # Unrequired
    period_start    = models.DateTimeField(u"開始時間", blank=True, null=True)
    period_end      = models.DateTimeField(u"終了時間", blank=True, null=True)
    place           = models.CharField(u"開催場所", max_length=255, blank=True)
    location        = GoogleMapField(u"地図", blank=True, query_field_id='id_place')
    # Uneditable
    author          = models.ForeignKey(User, verbose_name=u"主催者", related_name="events_owned", editable=False)
    members         = models.ManyToManyField(User, verbose_name=u"参加者", related_name="events_joined", null=True, editable=False)
    created_at      = models.DateTimeField(u"作成日時", auto_now_add=True)
    updated_at      = models.DateTimeField(u"更新日時", auto_now=True)
    publish_at      = models.DateTimeField(u"公開日時", null=True, editable=False)
    publish_at_date = models.DateField(u"公開日", null=True, editable=False)
    
    gcal            = models.URLField(verbose_name="GCalEditLink", blank=True, null=True, editable=False)
    
    tags            = TaggingField(related_name='blogs_entry_set')

    objects         = EventManager()
    
    class Meta:
        ordering            = ('period_start', 'period_end', '-publish_at', '-updated_at', 'title')
        verbose_name        = u"イベント"
        verbose_name_plural = verbose_name
        permissions         = (
            ('kick_event',       'Can kick user'),
            ('join_event',       'Can join event'),
        )
        
    def __unicode__(self):
        return self.title
        
    def clean(self, request=None):
        u"""各種Validation及び著者の自動設定"""
        # 公開日時・編集日時の設定およびバリデート
        if self.pub_state == u'draft' and self.publish_at:
            # 下書きが公開日時を持っているのはおかしな話なので None 設定を行う
            self.publish_at = None
            self.publish_at_date = None
        if self.pub_state != u'draft' and not self.publish_at:
            # 下書きから公開設定にされたときに公開日時を現在時刻に設定する
            self.publish_at = datetime.datetime.now()
            self.publish_at_date = datetime.datetime.now()
        # 開催場所・地図のバリデート
        if not self.place and self.location:
            raise ValidationError(u"開催場所が入力されていない状態で地図位置を指定することはできません。開催場所を指定するか地図を非表示にしてください")
        # 開催日時・終了日時のバリデート
        if self.period_start and self.period_end:
            if self.period_start > self.period_end:
                #終了時間が開始時間より先の場合はエラー
                raise ValidationError(u"開始日時を終了日時より後に設定することはできません")
            elif self.period_start < datetime.datetime.now() and (not self.pk or Event.objects.filter(pk=self.pk).count() == 0):
                # 過去のイベントかつこれが新規作成時（INSERT）だった場合はエラー
                raise ValidationError(u"過去のイベントを新規に作成することはできません")
            elif (self.period_end - self.period_start).days > 7:
                raise ValidationError(u'イベント期間が長すぎます')
        elif self.period_end and not self.period_start:
            # 終了時刻だけ設定されているのでエラー
            raise ValidationError(u"開始日時を設定してください")
        if self.pk is None:
            self.author = request.user if request else User.objects.get(pk=1)
        super(Event, self).clean(request)
        
    def save(self, request=None, action=None, *args, **kwargs):
        created = self.pk is None
        super(Event, self).save(request, *args, **kwargs)
        if created:
            self.members.add(self.author)
        if not action:
            site.get_backend(Event).autodiscover(self, created)
        
    def modify_object_permission(self, mediator, created):
        # Permission
        mediator.manager(self, self.author, ['events.kick_event', 'events.join_event'])
        if self.pub_state == 'public':
            mediator.viewer(self, None, ['events.join_event'])
            mediator.viewer(self, 'anonymous')
        elif self.pub_state == 'protected':
            mediator.viewer(self, None, ['events.join_event'])
            mediator.reject(self, 'anonymous')
        else:
            mediator.reject(self, None)
            mediator.reject(self, 'anonymous')
        
    def join(self, user, save=True):
        u"""イベントに参加する"""
        self.members.add(user)
        if save:
            self.save(action='join')
            site.get_backend(Event).autodiscover(self, 'join', user=user)
        
    def quit(self, user, save=True):
        u"""イベントの参加を取りやめる"""
        if user == self.author:
            raise AttributeError(u"Author doesn't allow to quit the event.")
        self.members.remove(user)
        if save:
            self.save(action='quit')
            site.get_backend(Event).autodiscover(self, 'quit', user=user)
        
    @models.permalink
    def get_absolute_url(self):
        if self.pub_state == 'draft':
            return ('events-event-update', (), {
                'object_id': self.pk,
            })
        return ('events-event-detail', (), {
            'object_id': self.pk,
        })
    
    def get_period_start_display(self):
        return u"%sから" % humanize_datetime(self.period_start, time=True)
   
    def get_period_display(self):
        u"""開催日時・終了日時を人間に読みやすいように表示する"""
        format = "%m/%d/(%a) %H:%M"
        ps = self.period_start
        pe = self.period_end
        
        if not ps:
            return u"開催日未定"
        else:
            if not pe:
                return u"%sから" % humanize_datetime(ps, time=True)
            else:
                if ps.year == pe.year and ps.month == pe.month:
                    return u"%sから%s" % (
                        humanize_datetime(ps, time=True),
                        humanize_relativedelta(relativedelta(pe, ps), with_suffix=False),
                    )
                else:
                    return u"%sから%sまで" %(
                        humanize_datetime(ps, time=True),
                        humanize_datetime(pe, time=True),
                    )
    get_period_display.short_description = u"イベント開催期間"
    
    def get_place_display(self):
        u"""場所を地図付き（可能ならば）で表示する"""
        if self.place:
            return mark_safe(u"""<p>%s</p>%s"""%(self.place, self.get_location_display))
        else:
            return u"開催地未定"
    get_place_display.short_description = u"イベント開催場所"
    
    def is_active(self):
        u"""イベントが終了したかどうかを返す"""
        if not self.period_start:
            return True
        return self.period_end >= datetime.datetime.now()
    is_active.short_description = u"イベントが終了していないかどうか"
    is_active.boolean = True

#
# Google Calender同期
#
from django.db.models.signals import post_save, pre_delete
from utils.gcal import update_gcal, delete_gcal
#if not settings.DEBUG:
post_save.connect(update_gcal, sender=Event)
pre_delete.connect(delete_gcal, sender=Event)
