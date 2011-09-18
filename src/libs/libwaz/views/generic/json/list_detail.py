# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/24
#
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage
from django.views.generic import list_detail
from django.core.exceptions import ObjectDoesNotExist

from libwaz.http import JsonResponse
from decorators import hand_response_method_to_kwargs
from utils import get_instance_json

@hand_response_method_to_kwargs
def object_list(request, method, *args, **kwargs):
    if method == 'json':
        queryset = kwargs['queryset']._clone()
        paginate_by = kwargs.get('paginate_by')
        page = kwargs.get('page')
        allow_empty = kwargs.get('allow_empty')
        if paginate_by:
            paginator = Paginator(queryset, paginate_by, allow_empty_first_page=allow_empty)
            if not page:
                page = request.GET.get('page', 1)
            try:
                page_number = int(page)
            except ValueError:
                if page == 'last':
                    page_number = paginator.num_pages
                else:
                    # Page is not 'last', nor can it be converted to an int.
                    raise Http404
            try:
                page_obj = paginator.page(page_number)
            except InvalidPage:
                raise Http404
            context = {
                'instance_list': [get_instance_json(instance) for instance in page_obj.object_list],
                'is_paginated': page_obj.has_other_pages(),
                'results_per_page': paginator.per_page,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'page': page_obj.number,
                'next': page_obj.next_page_number(),
                'previous': page_obj.previous_page_number(),
                'first_on_page': page_obj.start_index(),
                'last_on_page': page_obj.end_index(),
                'pages': paginator.num_pages,
                'hits': paginator.count,
                'page_range': paginator.page_range,
            }
            return JsonResponse(context)
        else:
            context = {
                'instance_list': [get_instance_json(instance) for instance in queryset],
                'is_paginated': False,
            }
        return JsonResponse(context)
    else:
        return list_detail.object_list(request, *args, **kwargs)

@hand_response_method_to_kwargs
def object_detail(request, method, *args, **kwargs):
    if method == 'json':
        queryset = kwargs['queryset']._clone()
        object_id = kwargs.get('object_id')
        slug = kwargs.get('slug')
        slug_field = kwargs.get('slug_field', 'slug')
        
        model = queryset.model
        if object_id:
            queryset = queryset.filter(pk=object_id)
        elif slug and slug_field:
            queryset = queryset.filter(**{slug_field: slug})
        else:
                raise AttributeError("Generic detail view must be called with either an object_id or a slug/slug_field.")
        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404("No %s found matching the query" % (model._meta.verbose_name))
        return JsonResponse({
            'instance': get_instance_json(obj)
        })
    else:
        return list_detail.object_detail(request, *args, **kwargs)