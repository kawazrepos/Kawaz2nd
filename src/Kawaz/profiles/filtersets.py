# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/03
#
from libwaz.contrib.siever import filters, filterset, widgets
from libwaz.contrib.tagging.filters import TaggingFilter

from models import Profile, Skill

class ProfileFilterSet(filterset.FilterSet):
    skills              = filters.ModelChoiceFilter(label=u"スキル", queryset=Skill.objects.all(), widget=widgets.LinkWidget())
    sex                 = filters.ChoiceFilter(label=u"性別", choices=[('', u"全て")] + list(Profile.SEX_TYPES), widget=widgets.LinkWidget())
    user__last_login    = filters.DateRangeFilter(label=u"最終ログイン", widget=widgets.LinkWidget())
    tags                = TaggingFilter(label=u"タグ", widget=widgets.LinkWidget())
    
    class Meta:
        model = Profile
        fields = ['skills', 'sex', 'user__last_login', 'tags']