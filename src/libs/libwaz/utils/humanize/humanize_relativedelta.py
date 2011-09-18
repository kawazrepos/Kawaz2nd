# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/16
#

__All__ = ['humanize_relativedelta']

def humanize_relativedelta(delta, more=False, with_suffix=True):
    u"""relativedeltaを人間に読みやすい形に修正して返す
    
    Example:
        >>> from dateutil.relativedelta import relativedelta
        >>> from datetime import datetime
        >>> NOW = datetime.now()
        >>> TODAY = datetime.today()
        >>> print humanize_relativedelta(relativedelta(years=2, months=2, days=2))
        2年後
        >>> print humanize_relativedelta(relativedelta(years=2, months=2, days=2), more=True)
        2年2ヶ月後
        >>> print humanize_relativedelta(relativedelta(years=-2, months=-2, days=-2))
        2年前
        >>> print humanize_relativedelta(relativedelta(years=-2, months=-2, days=-2), more=True)
        2年2ヶ月前
        >>> print humanize_relativedelta(relativedelta(months=2, days=2))
        2ヶ月後
        >>> print humanize_relativedelta(relativedelta(months=2, days=2), more=True)
        2ヶ月と2日後
        >>> print humanize_relativedelta(relativedelta(months=-2, days=-2))
        2ヶ月前
        >>> print humanize_relativedelta(relativedelta(months=-2, days=-2), more=True)
        2ヶ月と2日前
        >>> print humanize_relativedelta(relativedelta(days=2, hours=2))
        2日後
        >>> print humanize_relativedelta(relativedelta(days=2, hours=2), more=True)
        2日と2時間後
        >>> print humanize_relativedelta(relativedelta(days=-2, hours=-2))
        2日前
        >>> print humanize_relativedelta(relativedelta(days=-2, hours=-2), more=True)
        2日と2時間前
        >>> print humanize_relativedelta(relativedelta(hours=2, minutes=2))
        2時間後
        >>> print humanize_relativedelta(relativedelta(hours=2, minutes=2), more=True)
        2時間2分後
        >>> print humanize_relativedelta(relativedelta(hours=-2, minutes=-2))
        2時間前
        >>> print humanize_relativedelta(relativedelta(hours=-2, minutes=-2), more=True)
        2時間2分前
        >>> print humanize_relativedelta(relativedelta(minutes=2, seconds=2))
        2分後
        >>> print humanize_relativedelta(relativedelta(minutes=2, seconds=2), more=True)
        2分2秒後
        >>> print humanize_relativedelta(relativedelta(minutes=-2, seconds=-2))
        2分前
        >>> print humanize_relativedelta(relativedelta(minutes=-2, seconds=-2), more=True)
        2分2秒前
        >>> print humanize_relativedelta(relativedelta(seconds=2))
        2秒後
        >>> print humanize_relativedelta(relativedelta(seconds=-2))
        2秒前
    """
    if with_suffix:
        suffix = lambda x: u"後" if int(x) > 0 else u"前"
    else:
        suffix = lambda x: ""
    
    if abs(delta.years) > 0:
        if more:
            value = u"%s年%sヶ月%s" % (
                abs(delta.years),
                abs(delta.months),
                suffix(delta.years),
            )
        else:
            value = u"%s年%s" % (
                abs(delta.years),
                suffix(delta.years),
            )
    elif abs(delta.months) > 0:
        if more:
            value = u"%sヶ月と%s日%s" % (
                abs(delta.months),
                abs(delta.days),
                suffix(delta.months),
            )
        else:
            value = u"%sヶ月%s" % (
                abs(delta.months),
                suffix(delta.months),
            )
    elif abs(delta.days) > 0:
        if more:
            value = u"%s日と%s時間%s" % (
                abs(delta.days),
                abs(delta.hours),
                suffix(delta.days),
            )
        else:
            value = u"%s日%s" % (
                abs(delta.days),
                suffix(delta.days),
            )
    elif abs(delta.hours) > 0:
        if more:
            value = u"%s時間%s分%s" % (
                abs(delta.hours),
                abs(delta.minutes),
                suffix(delta.hours),
            )
        else:
            value = u"%s時間%s" % (
                abs(delta.hours),
                suffix(delta.hours),
            )
    elif abs(delta.minutes) > 0:
        if more:
            value = u"%s分%s秒%s" % (
                abs(delta.minutes),
                abs(delta.seconds),
                suffix(delta.minutes),
            )
        else:
            value = u"%s分%s" % (
                abs(delta.minutes),
                suffix(delta.minutes),
            )
    else:
        value = u"%s秒%s" % (
            abs(delta.seconds),
            suffix(delta.seconds),
        )
    return value

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()