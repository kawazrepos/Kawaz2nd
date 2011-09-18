# -*- coding: utf-8 -*-
#
# @author:    giginet
# @date:        2010/10/27
#
from libwaz.contrib.siever import filterset, filters, widgets
from libwaz.contrib.tagging.filters import TaggingFilter

from models import Material
from filters import FiletypeFilter

class MaterialFilterSet(filterset.FilterSetWithRequest):
    pub_state   = filters.ChoiceFilter(label=u"公開範囲", choices=[('', u"全て")]+list(Material.PUB_STATES), widget=widgets.LinkWidget())
    license     = filters.ChoiceFilter(label=u"ライセンス", choices=[('', u"全て")]+list(Material.LICENSES), widget=widgets.LinkWidget())
    filetype    = FiletypeFilter(label=u"ファイルタイプ", widget=widgets.LinkWidget())
    tags        = TaggingFilter(label=u"タグ", widget=widgets.LinkWidget())
    
    class Meta:
        model = Material
        fields = ['pub_state', 'license', 'tags']
