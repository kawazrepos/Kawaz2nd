# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/16
#
from django.utils.text import force_unicode

from datetime import datetime as _datetime
from dateutil.relativedelta import relativedelta as _relativedelta 

__ALL__ = ['humanize_datetime']

def humanize_datetime(datetime, weekday=True, time=False):
    u"""datetimeを人間が読みやすいように整形して表示する
    
    Example:
        >>> from datetime import datetime
        >>> from dateutil.relativedelta import relativedelta
        >>> TODAY = datetime.today()
        >>> print humanize_datetime(TODAY, extract_today=False)
        今日
        >>> # Delay with `seconds=+30`
        >>> print humanize_datetime(TODAY+relativedelta(hours=+2, seconds=+30), extract_today=True)
        2時間後
        >>> # Delay with `seconds=+30`
        >>> print humanize_datetime(TODAY-relativedelta(hours=+2, seconds=+30), extract_today=True)
        2時間前
    """
    TODAY = _datetime.today()
    date = force_unicode(datetime.strftime("%m/%d"))
    if weekday:
        weekday = force_unicode(datetime.strftime("(%a)"))
    else:
        weekday = u""
    if time:
        time = u" %s" % force_unicode(datetime.strftime("%H:%M"))
    else:
        time = u""
    if datetime.year == TODAY.year:
        if datetime.month == TODAY.month:
            if datetime.day == TODAY.day:
                return u"今日%s%s" % (weekday, time)
            elif datetime.day - TODAY.day == 1:
                return u"明日%s%s" % (weekday, time)
            elif datetime.day - TODAY.day == -1:
                return u"昨日%s%s" % (weekday, time)
            elif datetime.day - TODAY.day == 2:
                return u"明後日%s%s" % (weekday, time)
            elif datetime.day - TODAY.day == -2:
                return u"一昨日%s%s" % (weekday, time)
            elif datetime.day - TODAY.day == 7:
                return u"一週間後%s%s" % (weekday, time)
            elif datetime.day - TODAY.day == 7:
                return u"一週間前%s%s" % (weekday, time)
            else:
                delta = _relativedelta(datetime, TODAY)
                if delta.days > 0:
                    suffix = u"後"
                    days = delta.days
                else:
                    suffix = u"前"
                    days = abs(delta.days) + 1
                return u"%d日%s%s%s" % (days, suffix, weekday, time)
        else:
            return "%s%s%s" % (date, weekday, time)
    return "%s/%s%s%s" % (datetime.year, date, weekday, time)

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()