# -*- coding:utf-8 -*-
from django.template import RequestContext
from django.shortcuts import redirect, render_to_response
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import simple
from libwaz.views.generic import list_detail, create_update
from libwaz.contrib.object_permission.decorators import permission_required

from forms import MessageForm
from models import MessageState, Message
from filtersets import MessageRecivedFilterSet, MessageSentFilterSet

#
# list_detail
#-----------------------------------------------------------------------
@permission_required('messages.view_message')
def message_index(request):
    return simple.direct_to_template(request, r'messages/message_list.html')
@permission_required('messages.view_message')
def message_recived(request):
    kwargs = {
        'queryset': Message.objects.filter(recivers=request.user),
        'filter_class': MessageRecivedFilterSet,
        'template_name': r'messages/message_list_recived.html',
    }
    return list_detail.object_filter(request, **kwargs)
@permission_required('messages.view_message')
def message_sent(request):
    kwargs = {
        'queryset': Message.objects.filter(author=request.user),
        'filter_class': MessageSentFilterSet,
        'template_name': r'messages/message_list_sent.html',
    }
    return list_detail.object_filter(request, **kwargs)

@permission_required('messages.view_message', Message)
def message_detail(request, object_id):
    try:
        state = MessageState.objects.get(message__pk=object_id, user=request.user)
        if not state.read:
            state.read = True
            state.save()
    except MessageState.DoesNotExist:
        # 送信したメールだと既読管理オブジェクトは存在していない
        pass
    kwargs = {
        'queryset': Message.objects.published(request),
    }
    return list_detail.object_detail(request, object_id=object_id, **kwargs)

#
# create_update
#-------------------------------------------------------------------------
@permission_required('messages.add_message')
def create_message(request):
    if request.method == 'POST':
        form = MessageForm(request, request.POST)
        if form.is_valid():
            # オブジェクトを保存
            instance = Message.objects.create(
                author=request.user,
                title=form.cleaned_data['title'],
                body=form.cleaned_data['body'],
            )
            Message.objects.send(instance, form.cleaned_data['recivers'])
            # Email送信
            if form.cleaned_data.get('email', False):
                Message.objects.send_email(instance, form.cleaned_data['recivers'])
            return redirect(instance)
        else:
            recivers = request.POST.get('recivers', None)
    else:
        recivers = None
        to = request.GET.get('to', None)
        title = request.GET.get('title', None)
        if to or title:
            if to and to.startswith('group:'):
                group = to[6:]
                recivers = [user.pk for user in User.objects.filter(groups__name=group)]
            elif to:
                recivers = [user.pk for user in User.objects.filter(username=to)]
            else:
                recivers = []
            initial = {
                'recivers': recivers,
                'title': title or '',
            }
        else:
            initial = None
        form = MessageForm(request, initial=initial)
    kwargs = {
        'form': form,
        'recivers': recivers,
    }
    return render_to_response('messages/message_form.html', RequestContext(request, kwargs))

@permission_required('messages.delete_message', Message)
def delete_message(request, object_id):
    kwargs = {
        'model': Message,
        'post_delete_redirect': reverse('messages-message-list'),
    }
    return create_update.delete_object(request, object_id=object_id, **kwargs)