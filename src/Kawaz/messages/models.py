# -*- coding:utf-8 -*-
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from libwaz.db import models
from libwaz.db.models import Q
from libwaz.contrib.tagging.fields import TaggingField
from libwaz.contrib.object_permission import ObjectPermissionMediator
from libwaz.contrib.calls import site

from ..markitupfield.models import MarkItUpField


class MessageManager(models.Manager):
    
    def published(self, request=None):
        if request and request.user.is_authenticated():
            return self.filter(Q(author=request.user) | Q(recivers=request.user)).distinct()
        else:
            return self.none()

    def send_email(self, message, recivers):
        site = Site.objects.get_current()
        
        for reciver in recivers:
            ctx_dict = {'site': site, 'sender': message.author, 'reciver': reciver, 'message': message}
            subject = render_to_string('messages/message_email_subject.txt', ctx_dict)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            msg = render_to_string('messages/message_email.txt', ctx_dict)
        
            reciver.email_user(subject, msg)
        
    def send(self, message, recivers, email=False):
        pk_set = []
        for reciver in recivers:
            pk_set.append(reciver.pk)
            MessageState.objects.get_or_create(
                message=message,
                user=reciver
            )
            # メールが届いていることをCallする
            site.get_backend(Message).autodiscover(message, created=True, user_to=reciver)
        # Many to Manyを手動変更したのでシグナルを送信する
        m2m_changed.send(
            sender=Message.recivers.through,
            instance=message, 
            action='post_add',
            reverse=False,
            model=User,
            pk_set=pk_set)
        return message
    
class Message(models.ModelWithRequest):
    u"""メッセージモデル"""
    title           = models.CharField(u"タイトル", max_length=127)
    body            = MarkItUpField(u"本文", default_markup_type='markdown')
    recivers        = models.ManyToManyField(User, verbose_name=u"受信者" , related_name="recived_messages", through="MessageState")
    # Uneditable
    author          = models.ForeignKey(User, verbose_name=u"送信者", editable=False, related_name="sent_messages")
    created_at      = models.DateTimeField(u"作成日時", auto_now_add=True)
    updated_at      = models.DateTimeField(u"更新日時", auto_now=True)
    
    objects         = MessageManager()
    
    tags            = TaggingField()
    
    class Meta:
        ordering            = ('-created_at',)
        verbose_name        = u"メッセージ"
        verbose_name_plural = verbose_name
        permissions = (
            ('email_message',   'Can send email insted of message'),
        )
        
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ("messages-message-detail", (), {'object_id': self.pk})
    
    def clean(self, request=None):
        if self.pk is None:
            self.author = request.user if request else User.objects.get(pk=1)
        super(Message, self).clean(request)
    
    def modify_object_permission(self, mediator, created):
        # Permission
        mediator.manager(self, self.author)
        mediator.reject(self, None)
        mediator.reject(self, 'anonymous')

    def modify_object_permission_m2m(self, mediator, sender, model, pk_set, removed):
        if sender == self.recivers.through:
            for reciver in model.objects.filter(pk__in=pk_set):
                if not removed:
                    mediator.viewer(self, reciver)
                else:
                    mediator.reject(self, reciver)
            
class MessageState(models.Model):
    u"""メッセージ状態モデル"""
    message     = models.ForeignKey(Message, related_name="states")
    user        = models.ForeignKey(User)
    read        = models.BooleanField(u"既読フラグ", default=False)
    
    class Meta:
        verbose_name        = u"メッセージの状態"
        verbose_name_plural = verbose_name
    
    def get_absolute_url(self):
        return self.message.get_absolute_url()