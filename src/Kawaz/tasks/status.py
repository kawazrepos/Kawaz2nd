# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/04
#
class Status(object):
    def __init__(self, codename, verbose_name, help_text, do_verbose_name=None, do_help_text=None):
        self.codename = codename
        self.verbose_name = verbose_name
        self.help_text = help_text
        self._do_verbose_name = do_verbose_name
        self._do_help_text = do_help_text
    
    @property
    def do_verbose_name(self):
        if self._do_verbose_name:
            return self._do_verbose_name
        return self.verbose_name
    @property
    def do_help_text(self):
        if self._do_help_text:
            return self._do_help_text
        return self.help_text
    def __repr__(self):
        return self.codename
    def __unicode__(self):
        return unicode(self.verbose_name)
    def __str__(self):
        return self.__unicode__().encode('utf-8')
    
    def __eq__(self, other):
        if isinstance(other, Status):
            return self.codename == other.codename
        else:
            return self.codename == other
    def __ne__(self, other):
        raise NotImplementedError
        
NEW         = Status('new', u"認証待ち", u"担当者がタスクを認証するのを待っています", do_verbose_name=u"再開", do_help_text=u"完了したタスクを再開します")
CANCELED    = Status('canceled', u"キャンセル", u"全ての担当者がタスクをキャンセルしました", do_verbose_name=u"担当から外れる", do_help_text=u"タスク担当者から外れます")
ACCEPTED    = Status('accepted', u"作業中", u"担当者がタスクを確認し現在作業中です", do_verbose_name=u"認証・再開", do_help_text=u"タスクを認証して作業に移ります")
REJECTED    = Status('rejected', u"再作業要請", u"発行者が作業の完了を拒否し再作業を要求しています", do_help_text=u"担当者に再作業を要請します")
PAUSED      = Status('paused', u"一時停止中", u"作業を一時停止中です", do_verbose_name=u"一時停止", do_help_text=u"作業を一時停止します")
DONE        = Status('done', u"作業終了", u"作業が終了し発行者の確認待ちです", do_help_text=u"作業が完了したことを発行者に伝え確認を待ちます")
FROZEN      = Status('frozen', u"凍結中", u"発行者がタスクを凍結しています", do_verbose_name=u"凍結", do_help_text=u"タスクを凍結します")
CLOSED      = Status('closed', u"完了", u"発行者がタスクの完了を確認しました", do_help_text=u"タスクを閉じます")

STATUSES = (
    (NEW.codename, NEW.verbose_name),
    (CANCELED.codename, CANCELED.verbose_name),
    (ACCEPTED.codename, ACCEPTED.verbose_name),
    (REJECTED.codename, REJECTED.verbose_name),
    (PAUSED.codename, PAUSED.verbose_name),
    (DONE.codename, DONE.verbose_name),
    (FROZEN.codename, FROZEN.verbose_name),
    (CLOSED.codename, CLOSED.verbose_name),
)
STATUSES_DICT = {
    NEW.codename: NEW,
    CANCELED.codename: CANCELED,
    ACCEPTED.codename: ACCEPTED,
    REJECTED.codename: REJECTED,
    PAUSED.codename: PAUSED,
    DONE.codename: DONE,
    FROZEN.codename: FROZEN,
    CLOSED.codename: CLOSED,
}