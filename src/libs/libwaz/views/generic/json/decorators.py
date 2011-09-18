# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/24
#
def hand_response_method_to_kwargs(fn):
    u"""クライアントが期待しているレスポンスの形式情報をGET/POSTから取得してkwargsに投げるデコレータ"""
    def inner(request, *args, **kwargs):
        if 'method' in request.REQUEST:
            kwargs['method'] = request.REQUEST['method']
        elif not 'method' in kwargs:
            kwargs['method'] = None
        return fn(request, *args, **kwargs)
    return inner