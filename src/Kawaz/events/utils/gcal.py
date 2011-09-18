# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/13
#
#
# Google Calender連携
#
from django.conf import settings
from django.utils.html import strip_tags

import atom
import gdata.service
import gdata.calendar.service

def _login_gcal(email = None, password=None):
    u"""
    Login to Google Calender with GCAL_LOGIN_EMAIL, GCAL_LOGIN_PASS
    """
    if not email: email = settings.GCAL_LOGIN_EMAIL
    if not password: password = settings.GCAL_LOGIN_PASS
    client = gdata.calendar.service.CalendarService()
    client.email = email
    client.password = password
    client.ProgrammaticLogin()
    return client

def update_gcal(sender, instance, created, **kwargs):
    #
    #    イベント作成、更新時にGoogleカレンダーとの同期を行うシグナル
    #    同期先のカレンダーはsettings.GCAL_CALENDAR_IDに依存する
    #
    #新規作成時の処理。イベントに作成日、終了日が設定されているときのみ同期を行う
    if instance.period_start and instance.period_end and instance.pub_state != 'draft':
        #イベントの新規作成時の処理
        try:
            client = _login_gcal()
        except gdata.service.BadAuthentication:
            return
        #既存のカレンダーを一度削除
        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text=instance.title)
        event.content = atom.Content(text=strip_tags(instance.body.rendered))
        event.where.append(gdata.calendar.Where(value_string=instance.place))
        start_time = instance.period_start.strftime('%Y-%m-%dT%H:%M:%S.000+09:00')
        end_time = instance.period_end.strftime('%Y-%m-%dT%H:%M:%S.000+09:00')
        event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
        #インスタンスに、Googleイベントが結びついていないときは新規作成
        if not instance.gcal:
            try:
                new_event = client.InsertEvent(event, ('/calendar/feeds/%s/private/full' % settings.GCAL_CALENDAR_ID))
                instance.gcal = new_event.GetEditLink().href
                instance.save()
            except:
                pass
        elif not created:
            #結びついているときは更新してやる
            try:
                client.UpdateEvent(instance.gcal, event)
            except:
                pass
    elif instance.gcal:
        #日付が未設定かつ、すでにイベントが作成済みの時、イベント削除。
        instance.gcal = None
        instance.save()
        try:
            client.DeleteEvent(instance.gcal)
        except:
            pass
        
def delete_gcal(sender, instance, **kwargs):
    try:
        #GoogleCalendarからイベントを削除
        if instance.gcal:
            client = _login_gcal()
            client.DeleteEvent(instance.gcal)
    except:
        # とりあえず動かないことばっかりだから Fail silentlyにしとく
        pass
