# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/27
#
# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/11
#
from django.utils.safestring import mark_safe

from libwaz.contrib.history import site
from libwaz.contrib.history import backends

from models import Material

class MaterialHistoryBackend(backends.BasicHistoryBackend):
    def _post_save_callback(self, *args, **kwargs):
        pass
    def get_message(self, timeline):
        if timeline.action == 'create':
            kwargs = {
                'user': self.get_user(timeline),
                'label': self.get_label(timeline)
            }
            return mark_safe(u"%(user)sさんが「%(label)s」をアップロードしました" % kwargs)
        else:
            return super(MaterialHistoryBackend, self).get_message(timeline)
        
site.register(Material, MaterialHistoryBackend)