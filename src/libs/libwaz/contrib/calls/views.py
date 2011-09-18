# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/13
#
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import simple
from django.utils.translation import ugettext_lazy as _

from models import Call

@login_required
def clear_calls(request, notify=True):
    next = request.REQUEST.get('next', '/')
    qs = Call.objects.filter(user_to=request.user)
    if request.method == 'POST':
        for call in qs:
            call.read = True
            call.save()
        if notify:
            messages.success(request, _(u"Calls are successfully cleared."), fail_silently=True)
        return redirect(next)
    else:
        kwargs = {
            'template': r'calls/calls_confirm_clear.html',
        }
        return simple.direct_to_template(request, **kwargs)