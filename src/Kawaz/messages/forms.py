# -*- coding: utf-8 -*-
from libwaz import forms

from ..profiles.models import Profile

from models import Message

class MessageForm(forms.ModelFormWithRequest):
    class Meta:
        model = Message
        fields = ('recivers', 'title', 'body')
    
    def __init__(self, request, *args, **kwargs):
        super(MessageForm, self).__init__(request, *args, **kwargs)
        self.fields['recivers'].queryset = Profile.objects.published(request).exclude(user=request.user)
        
        if request.user.has_perm('messages.email_message'):
            self.fields['email'] = forms.BooleanField(label=u"メッセージのコピーを登録メールに送信する", required=False,
                                                      help_text=u"受信者全員の登録メールアドレスにメッセージの内容を転送します。送信元はKawazになります。"
                                                      u"またメッセージ本文はHTML形式ではなくMarkdown形式で送られるので注意してください。")
        
    def save(self, commit=True):
        # メッセージは通常の保存では不可能なので呼び出された場合はエラーを発生させる
        raise NotImplementedError
    
    def clean_recivers(self):
        _recivers = self.cleaned_data['recivers']
        recivers = []
        for reciver in _recivers:
            if isinstance(reciver, Profile):
                recivers.append(reciver.user)
            else:
                recivers.append(reciver)
        return recivers