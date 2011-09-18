# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

from models import Draft

@login_required
def draft_list(request):
    drafts = Draft.objects.all(request)
    dict_info = {
        'template': r"drafts/draft_list.html",
        'extra_context': {
            'drafts': drafts
        }
    }
    return direct_to_template(request, **dict_info)