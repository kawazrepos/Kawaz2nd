# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
u"""

`date_based` generic view avariable to use `paginate_by`
arguments like `list_detail.object_list`

"""
from list_detail import object_list
from list_detail import object_detail as _object_detail

import datetime
from dateutil.relativedelta import relativedelta

__all__ = [
    'date_based', 'archive_index', 
    'archive_year', 'archive_month',
    'archive_week', 'archive_day',
    'archive_today', 'object_detail'
]

def date_based(fn):
    u"""
    filtering queryset with `date_based` arguments
    
    WARNING:
        kwargs for `date_based` is handed to the function for generating extra_context
        make sure to remove these arguments when you put the `kwargs` to `list_detail`
        function
    """
    def inner(request, *args, **kwargs):
        # Validation
        if not 'queryset' in kwargs:
            raise AttributeError(u"You cannot use 'date_based' decorator for function which doesn't have 'queryset' in 'kwargs'")
        if not 'date_field' in kwargs:
            raise AttributeError(u"You cannot use 'date_based' decorator for function which doesn't have 'date_field' in 'kwargs'")
        date_field = kwargs['date_field']
        queryset = kwargs['queryset']
        if 'year' in kwargs:
            queryset = queryset.filter(**{"%s__year"%date_field: kwargs.get('year')})
        if 'month' in kwargs:
            # TODO: Check 'month_format' and change the way to filter
            queryset = queryset.filter(**{"%s__month"%date_field: kwargs.get('month')})
        if 'day' in kwargs:
            # TODO: Chekc 'day_foramt' and change the way to filter
            queryset = queryset.filter(**{"%s__day"%date_field: kwargs.get('day')})
        if not kwargs.get('allow_future'):
            queryset = queryset.exclude(**{"%s__gt"%date_field: datetime.datetime.now()})
        kwargs['queryset'] = queryset
        return fn(request, *args, **kwargs)
    return inner

def template_name(template_name):
    u"""
    overwrite default templatename for generic view
    """
    def inner(fn):
        def inner2(request, *args, **kwargs):
            if 'queryset' in kwargs:
                queryset = kwargs['queryset']
            elif 'model' in kwargs:
                queryset = kwargs['model'].objects
            elif 'form_class' in kwargs:
                queryset = kwargs['form_class']._meta.model.objects
            if not 'template_name' in kwargs:
                kwargs['template_name'] = template_name % {
                'app_label': queryset.model._meta.app_label,
                'model_name': queryset.model._meta.object_name.lower(),
            }
            return fn(request, *args, **kwargs)
        return inner2
    return inner

def _remove_surplus_kwargs(kwargs):
    u"""
    remove all surplus kwargs.
    """
    surpluses = (
        'date_field', 'year', 'month', 'day', 'week',
        'allow_future',
        'month_format', 'day_format',
    )
    for surplus in surpluses:
        if surplus in kwargs: kwargs.pop(surplus)
    return kwargs

@date_based
def object_detail(request, *args, **kwargs):
    kwargs = _remove_surplus_kwargs(kwargs)
    return _object_detail(request, *args, **kwargs)

@template_name(r"%(app_label)s/%(model_name)s_archive.html")
@date_based
def archive_index(request, *args, **kwargs):
    """
    Generic top-level paginatable archive of date-based objects.

    Templates: ``<app_label>/<model_name>_archive.html``
    Context:
        date_list
            List of years
        latest
            Latest N (defaults to 15) objects by date
    """
    NUM_LATEST = 15
    # Create context for `date_based.archive_index`
    extra_context = kwargs.get('extra_context', {})
    extra_context.update({
        'date_list': kwargs['queryset'].dates(kwargs['date_field'], 'year')[::-1],
        # add `latest` for make it handy.
        # Notice:
        #  set `latest` to `template_object_name` doesn't work as expect
        #  see  http://docs.djangoproject.com/en/1.2/ref/generic-views/
        'latest': kwargs['queryset'][:kwargs.get('num_latest', NUM_LATEST)],
    })
    kwargs['extra_context'] = extra_context
    kwargs = _remove_surplus_kwargs(kwargs)
    return object_list(request, *args, **kwargs)

@template_name(r"%(app_label)s/%(model_name)s_archive_year.html")
@date_based
def archive_year(request, *args, **kwargs):
    """
    Generic paginatable yearly archive view.

    Templates: ``<app_label>/<model_name>_archive_year.html``
    Context:
        date_list
            List of months in this year with objects
        year
            This year
        object_list
            List of objects published in the given month
            (Only available if make_object_list argument is True)
    """
    # Create context for `date_based.archive_index`
    extra_context = kwargs.get('extra_context', {})
    extra_context.update({
        'date_list': kwargs['queryset'].dates(kwargs['date_field'], 'month')[::-1],
        'year': kwargs['year'],
    })
    kwargs['extra_context'] = extra_context
    kwargs = _remove_surplus_kwargs(kwargs)
    return object_list(request, *args, **kwargs)

@template_name(r"%(app_label)s/%(model_name)s_archive_month.html")
@date_based
def archive_month(request, *args, **kwargs):
    """
    Generic paginatable monthly archive view.

    Templates: ``<app_label>/<model_name>_archive_month.html``
    Context:
        date_list:
            List of days in this month with objects
        month:
            (date) this month
        next_month:
            (date) the first day of the next month, or None if the next month is in the future
        previous_month:
            (date) the first day of the previous month
        object_list:
            list of objects published in the given month
    """
    # Calculate the date with current time
    month = datetime.date(int(kwargs['year']), int(kwargs['month']), 1)
    if month >= datetime.date(datetime.date.today().year, datetime.date.today().month, 1):
        next_month = None
    else:
        next_month = month + relativedelta(months=1)
        next_month = datetime.date(next_month.year, next_month.month, 1)
    previous_month = month - relativedelta(months=1)
    previous_month = datetime.date(previous_month.year, previous_month.month, 1)
    # Create context for `date_based.archive_index`
    extra_context = kwargs.get('extra_context', {})
    extra_context.update({
        'date_list': kwargs['queryset'].dates(kwargs['date_field'], 'month')[::-1],
        'month': month,
        'next_month': next_month,
        'previous_month': previous_month,
    })
    kwargs['extra_context'] = extra_context
    kwargs = _remove_surplus_kwargs(kwargs)
    return object_list(request, *args, **kwargs)

@template_name(r"%(app_label)s/%(model_name)s_archive_week.html")
@date_based
def archive_week(request, *args, **kwargs):
    """
    Generic paginatable weekly archive view.

    Templates: ``<app_label>/<model_name>_archive_week.html``
    Context:
        week:
            (date) this week
        object_list:
            list of objects published in the given week
    
    WARNING:
        this method doesn't work yet.
    """
    # TODO: Code it
    import warnings
    warnings.warn(u"'archive_week' method has not coded yet.")
    kwargs = _remove_surplus_kwargs(kwargs)
    return object_list(request, *args, **kwargs)

@template_name(r"%(app_label)s/%(model_name)s_archive_day.html")
@date_based
def archive_day(request, *args, **kwargs):
    """
    Generic paginatable daily archive view.

    Templates: ``<app_label>/<model_name>_archive_day.html``
    Context:
        object_list:
            list of objects published that day
        day:
            (datetime) the day
        previous_day
            (datetime) the previous day
        next_day
            (datetime) the next day, or None if the current day is today
    """
    # Calculate day with current time
    day = datetime.date(int(kwargs['year']), int(kwargs['month']), int(kwargs['day']))
    if day >= datetime.date.today():
        next_day = None
    else:
        next_day = day + relativedelta(days=1)
    previous_day = day - relativedelta(days=1)
    # Create context for `date_based.archive_index`
    extra_context = kwargs.get('extra_context', {})
    extra_context.update({
        'day': day,
        'next_day': next_day,
        'previous_day': previous_day,
    })
    kwargs = _remove_surplus_kwargs(kwargs)
    return object_list(request, *args, **kwargs)

def archive_today(request, *args, **kwargs):
    """
    Generic paginatable daily archive view for today. Same as archive_day view.
    """
    today = datetime.date.today()
    kwargs['year'] = today.year
    kwargs['month'] = today.month
    kwargs['day'] = today.day
    return archive_day(request, *args, **kwargs)