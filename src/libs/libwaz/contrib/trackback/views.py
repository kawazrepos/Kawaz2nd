# -*- coding: utf-8 -*-
#
# @date:        2010/09/26
# @author:    alisue
#
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_exempt

from forms import TrackbackForm

@csrf_exempt
@require_POST
def receive_trackback(request, ctype_id, object_id, form_class=TrackbackForm, template_name=r"trackback/trackback_response.xml"):
    ctype = get_object_or_404(ContentType, pk=ctype_id)
    obj = get_object_or_404(ctype.model_class(), pk=object_id)
    site = Site.objects.get_current()
    form = form_class(request.POST)
    if form.is_valid():
        trackback = form.save(commit=False)
        trackback.content_object = obj
        trackback.remote_ip = request.META['REMOTE_ADDR']
        trackback.site = site
        trackback.save()
        return render_to_response(template_name, {'error': False})
    else:
        context = {
            'error': True,
            'message': "\n".join([u"%s: %s" % (k, v) for k, v in form.errors.iteritems()])
        }
        return render_to_response(template_name, context)