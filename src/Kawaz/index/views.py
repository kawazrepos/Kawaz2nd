# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.http import Http404

from ..tweets.forms import TweetForm
from ..tweets.models import Tweet

def index(request):
    if request.user.is_authenticated():
        dict_info = {
            'template':         r"index/authenticated.html",
            'extra_context':    {
                'tweet_form':    TweetForm(request=request),
                'tweets':        Tweet.objects.all(),
            }
        }
    elif settings.DEBUG:
        dict_info = {
            'template':         r"index/anonymous.html",
            'extra_context':    {
                'tweets':        Tweet.objects.all(),
            }
        }
    else:
        raise Http404
    return direct_to_template(request, **dict_info)