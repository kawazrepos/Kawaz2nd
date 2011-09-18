# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import simple
from django.contrib import messages

from libwaz.http import Http403
from models import MarkItUpComment

def delete_comment(request, object_id):
    obj = get_object_or_404(MarkItUpComment, pk=object_id)
    if obj.user: 
        if obj.user != request.user and not request.user.is_superuser:
            raise Http403
    else:
        if not request.user.is_staff:
            raise Http403
    if request.method == 'POST':
        obj.is_removed = True
        obj.save()
        msg = u"コメントを削除しました"
        messages.success(request, msg, fail_silently=True)
        return redirect(obj)
    else:
        kwargs = {
            'template': r"comments/delete.html",
            'extra_context': {
                'object': obj,
            }
        }
        return simple.direct_to_template(request, **kwargs)
