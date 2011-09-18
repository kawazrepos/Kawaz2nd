# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags


from libwaz.http import JsonResponse
from libwaz.views.generic import list_detail
from libwaz.views.generic import create_update
from libwaz.contrib.object_permission.decorators import permission_required

from models import Tweet
from forms import FavoriteTweetForm, TweetForm

def withauthor(fn):
    def inner(request, *args, **kwargs):
        if 'author' in kwargs:
            if not isinstance(kwargs['author'], User):
                author = get_object_or_404(User, username=kwargs['author'])
                kwargs['author'] = author
        else:
            kwargs['author'] = None
        return fn(request, *args, **kwargs)
    return inner

#
# list_detail
#--------------------------------------------------------------------------------------
@withauthor
def tweet_list(request, author=None):
    kwargs = {
        'queryset': Tweet.objects.all() if not author else Tweet.objects.filter(author=author),
        'paginate_by': settings.DEFAULT_TIMELINE_LENGTH,
        'extra_context': {
            'author': author,
        },
    }
    return list_detail.object_list(request, **kwargs)
@withauthor
def tweet_favorite_list(request, author=None, order_by='new', threshold=3):
    qs = Tweet.objects.annotate(favorite_users=Count('users'))
    # Author filter
    if author:
        qs = qs.filter(author=author)
    # Threshold filter
    qs = qs.filter(favorite_users__gte=threshold)
    # Order by
    if order_by == 'popular':
        qs = qs.order_by('-favorite_users', '-created_at')
    elif order_by == 'new':
        qs = qs.order_by('-created_at', '-favorite_users')
    kwargs = {
        'queryset': qs,
        'template_name': r'tweets/tweet_favorite_list.html',
        'extra_context': {
            'author': author,
            'threshold': threshold,
            'order_by': order_by,
        }
    }
    return list_detail.object_list(request, **kwargs)
@permission_required('tweets.view_tweet', Tweet)
@withauthor
def tweet_detail(request, author, object_id):
    kwargs = {
        'queryset': Tweet.objects.filter(author=author),
        'extra_context': {
            'author': author,
        },
    }
    return list_detail.object_detail(request, object_id=object_id, **kwargs)

#
# create_update
#-----------------------------------------------------------------------------------------
@permission_required('tweets.add_tweet')
def create_tweet(request):
    kwargs = {
        'form_class': TweetForm,
        'post_save_redirect': '/',
    }
    return create_update.create_object(request, **kwargs)
@permission_required('tweets.delete_tweet', Tweet)
def delete_tweet(request, object_id):
    kwargs = {
        'model': Tweet,
        'post_delete_redirect': reverse('tweets-tweet-list'),
    }
    return create_update.delete_object(request, object_id=object_id, **kwargs)

#
# API
#-----------------------------------------------------------------------------------------
@require_POST
@csrf_protect
@login_required
def favorite_tweet(request):
    form = FavoriteTweetForm(request.POST)
    if form.is_valid():
        object_id = form.cleaned_data['object_id']
        obj = get_object_or_404(Tweet, pk=object_id)
        if request.user in obj.users.all():
            obj.users.remove(request.user)
            action = 'removed'
        else:
            obj.users.add(request.user)
            action = 'add'
        obj.save()
        data = {
            'state': 'OK', 
            'action': action, 
            'user': {
                'pk':request.user.pk,
                'username':request.user.get_profile().nickname,
                'href':request.user.get_absolute_url(),
                'icon':request.user.get_profile().get_icon_small_display()
            }
        }
        return JsonResponse(data)
    else:
        data = {
            'state': 'Failed',
            'errors': "¥n".join([strip_tags("%s: %s" % (k, v)) for k, v in form.errors.iteritems()])
        }
        return JsonResponse(data)
