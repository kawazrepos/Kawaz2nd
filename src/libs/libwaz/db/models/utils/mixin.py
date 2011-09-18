# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
# from snippets: http://djangosnippets.org/snippets/2249/
#
##############
#  utils.py  #
##############
__all__ = ['ModelMixin']

class MixinType(type):
    def __new__(cls, name, bases, dct):
        ret = type.__new__(cls, name, bases, dct)

        if name != 'ModelMixin':
            assert 'model' in dct
            model = dct.pop('model')

            for k, v in dct.iteritems():
                if k not in ModelMixin.__dict__:
                    model.add_to_class(k, v)

        return ret


class ModelMixin(object):
    __metaclass__ = MixinType


################
##  models.py  #
################
#
#class UserMixin(ModelMixin):
#    model = User
#
#    @property
#    def foobar(user):
#        try:
#            return user.foobar_set.get()
#        except Foobar.DoesNotExist:
#            return None
#
#    @property
#    def is_boss(user):
#        return user.foobar is not None
#
#    def __unicode__(user):
#        try:
#            profile = user.get_profile()
#            if profile.full_name:
#                return profile.full_name
#
#        except UserProfile.DoesNotExist:
#            pass
#
#        full_name = (u'%s %s' % (user.first_name, user.last_name)).strip()
#        if full_name:
#            return full_name
#
#        return user.username
#
#    def get_absolute_url(user):
#        return reverse('localsite_user_detail', kwargs=dict(username=user.username))