# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.comments.models import Comment
from django.contrib.comments.models import BaseCommentAbstractModel,COMMENT_MAX_LENGTH,CommentManager
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from ..markitupfield.models import MarkItUpField

from datetime import datetime

class MarkItUpComment(BaseCommentAbstractModel):
    """
    A user comment about some object.
    """

    # Who posted this comment? If ``user`` is set then it was an authenticated
    # user; otherwise at least user_name should have been set and the comment
    # was posted by a non-authenticated user.
    user        = models.ForeignKey(User, verbose_name=_('user'),
                    blank=True, null=True, related_name="%(class)s_comments")
    user_name   = models.CharField(_("user's name"), max_length=50, blank=True)
    user_email  = models.EmailField(_("user's email address"), blank=True, null=True)
    user_url    = models.URLField(_("user's URL"), blank=True, null=True)

    comment     = MarkItUpField(default_markup_type='comment_markdown')

    # Metadata about the comment
    submit_date = models.DateTimeField(_('date/time submitted'), default=None)
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True)
    is_public   = models.BooleanField(_('is public'), default=True,
                    help_text=_('Uncheck this box to make the comment effectively ' \
                                'disappear from the site.'))
    is_removed  = models.BooleanField(_('is removed'), default=False,
                    help_text=_('Check this box if the comment is inappropriate. ' \
                                'A "This comment has been removed" message will ' \
                                'be displayed instead.'))

    # Manager
    objects = CommentManager()

    class Meta:
        ordering            = ('submit_date',)
        permissions         = [("can_moderate", "Can moderate comments")]
        verbose_name        = _('comment')
        verbose_name_plural = _('comments')

    def __unicode__(self):
        return u"%s: %s" % (self.name, self.content_object)

    def save(self, *args, **kwargs):
        if self.submit_date is None:
            self.submit_date = datetime.datetime.now()
        super(MarkItUpComment, self).save(*args, **kwargs)

    def _get_userinfo(self):
        """
        Get a dictionary that pulls together information about the poster
        safely for both authenticated and non-authenticated comments.

        This dict will have ``name``, ``email``, and ``url`` fields.
        """
        if not hasattr(self, "_userinfo"):
            self._userinfo = {
                "name"  : self.user_name,
                "email" : self.user_email,
                "url"   : self.user_url
            }
            if self.user_id:
                u = self.user
                if u.email:
                    self._userinfo["email"] = u.email

                # If the user has a full name, use that for the user name.
                # However, a given user_name overrides the raw user.username,
                # so only use that if this comment has no associated name.
                if u.get_full_name():
                    self._userinfo["name"] = self.user.get_full_name()
                elif not self.user_name:
                    self._userinfo["name"] = u.username
        return self._userinfo
    userinfo = property(_get_userinfo, doc=_get_userinfo.__doc__)

    def _get_name(self):
        return self.userinfo["name"]
    def _set_name(self, val):
        if self.user_id:
            raise AttributeError(_("This comment was posted by an authenticated "\
                                   "user and thus the name is read-only."))
        self.user_name = val
    name = property(_get_name, _set_name, doc="The name of the user who posted this comment")

    def _get_email(self):
        return self.userinfo["email"]
    def _set_email(self, val):
        if self.user_id:
            raise AttributeError(_("This comment was posted by an authenticated "\
                                   "user and thus the email is read-only."))
        self.user_email = val
    email = property(_get_email, _set_email, doc="The email of the user who posted this comment")

    def _get_url(self):
        return self.userinfo["url"]
    def _set_url(self, val):
        self.user_url = val
    url = property(_get_url, _set_url, doc="The URL given by the user who posted this comment")

    def get_absolute_url(self, anchor_pattern="#c%(id)s"):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)

    def get_as_text(self):
        """
        Return this comment as plain text.  Useful for emails.
        """
        d = {
            'user': self.user or self.name,
            'date': self.submit_date,
            'comment': self.comment.raw,
            'domain': self.site.domain,
            'url': self.get_absolute_url()
        }
        return _('Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s') % d
    
#from django.contrib.comments.signals import comment_will_be_posted
#from libwaz.utils.akismet import on_comment_will_be_posted
#comment_will_be_posted.connect(on_comment_will_be_posted)
