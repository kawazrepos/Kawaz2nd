# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/25
#
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic import simple

from libwaz.http import Http403
from libwaz.views.generic import list_detail
from libwaz.views.generic import create_update
from libwaz.contrib.object_permission.decorators import permission_required

from models import Component, Version, Report, Product
from forms import ComponentForm, VersionForm,  ProductForm
from forms import ReportForm, ReportFormForAnonymous, ReportFormForStatus
from filterset import ReportFilterSet

def withproduct(fn):
    def inner(request, *args, **kwargs):
        if 'product' in kwargs:
            product = kwargs['product']
            if not isinstance(product, Product):
                product = get_object_or_404(Product, pk=product)
            kwargs['product'] = product
        return fn(request, *args, **kwargs)
    return inner
#
# list_detail
#----------------------------------------------------------------
@withproduct
def component_list(request, product):
    kwargs = {
        'queryset': Component.objects.filter(product=product),
        'extra_context': {
            'product': product,
        }
    }
    return list_detail.object_list(request, **kwargs)
@withproduct
def version_list(request, product):
    kwargs = {
        'queryset': Version.objects.filter(product=product),
        'extra_context': {
            'product': product,
        }
    }
    return list_detail.object_list(request, **kwargs)
@withproduct
def report_list(request, product):
    kwargs = {
        'queryset': Report.objects.filter(product=product),
        'filter_class': ReportFilterSet,
        'initial': {
            'product': product,
        },
        'extra_context': {
            'product': product,
        }
    }
    return list_detail.object_filter(request, **kwargs)
def product_list(request):
    kwargs = {
        'queryset': Product.objects.all(),
    }
    return list_detail.object_list(request, **kwargs)
@withproduct
def component_detail(request, product, object_id):
    obj = get_object_or_404(Component, pk=object_id)
    kwargs = {
        'queryset': Component.objects.filter(product=product),
        'extra_context': {
            'product': product,
            'active_reports': obj.reports.exclude(status='verified'),
            'verified_reports': obj.reports.filter(status='verified'),
        }
    }
    return list_detail.object_detail(request, object_id=object_id, **kwargs)
@withproduct
def version_detail(request, product, object_id):
    obj = get_object_or_404(Version, pk=object_id)
    kwargs = {
        'queryset': Version.objects.filter(product=product),
        'extra_context': {
            'product': product,
            'active_reports': obj.reports.exclude(status='verified'),
            'verified_reports': obj.reports.filter(status='verified'),
        }
    }
    return list_detail.object_detail(request, object_id=object_id, **kwargs)
@withproduct
def report_detail(request, product, object_id):
    kwargs = {
        'queryset': Report.objects.filter(product=product),
        'extra_context': {
            'product': product,
        }
    }
    return list_detail.object_detail(request, object_id=object_id, **kwargs)
def product_detail(request, object_id):
    obj = get_object_or_404(Product, pk=object_id)
    kwargs = {
        'queryset': Product.objects.all(),
        'extra_context': {
            'active_reports': obj.reports.exclude(status='verified'),
            'verified_reports': obj.reports.filter(status='verified'),
        }
    }
    return list_detail.object_detail(request, object_id=object_id, **kwargs)

#
# create_update
#-------------------------------------------------------------------------
@permission_required('bugwaz.add_component')
@withproduct
def create_component(request, product):
    if not request.user.has_perm('bugwaz.add_component_product', product):
        raise Http403
    kwargs = {
        'form_class': ComponentForm,
        'initial': {
            'product': product.pk,
        },
        'extra_context': {
            'product': product,
        }
    }
    return create_update.create_object(request, **kwargs)
@permission_required('bugwaz.add_version')
@withproduct
def create_version(request, product):
    if not request.user.has_perm('bugwaz.add_version_product', product):
        raise Http403
    kwargs = {
        'form_class': VersionForm,
        'initial': {
            'product': product.pk,
        },
        'extra_context': {
            'product': product,
        }
    }
    return create_update.create_object(request, **kwargs)
@withproduct
def create_report(request, product):
    if request.user.is_authenticated():
        kwargs = {
            'form_class': ReportForm,
            'initial': {
                'product': product.pk,
                'username': request.user.get_profile().nickname,
            },
            'extra_context': {
                'product': product,
            }
        }
    else:
        kwargs = {
            'form_class': ReportFormForAnonymous,
            'initial': {
                'product': product.pk,
            },
            'extra_context': {
                'product': product,
            }
        }
    return create_update.create_object(request, **kwargs)
@permission_required('bugwaz.add_product')
def create_product(request):
    kwargs = {
        'form_class': ProductForm,
    }
    return create_update.create_object(request, **kwargs)
@permission_required('bugwaz.change_component', Component)
@withproduct
def update_component(request, product, object_id):
    kwargs = {
        'form_class': ComponentForm,
        'extra_context': {
            'product': product,
        }
    }
    return create_update.update_object(request, object_id=object_id, **kwargs)
@permission_required('bugwaz.change_version', Version)
@withproduct
def update_version(request, product, object_id):
    kwargs = {
        'form_class': VersionForm,
        'extra_context': {
            'product': product,
        }
    }
    return create_update.update_object(request, object_id=object_id, **kwargs)
@permission_required('bugwaz.change_report', Report)
@withproduct
def update_report(request, product, object_id):
    kwargs = {
        'form_class': ReportForm,
        'extra_context': {
            'product': product,
        }
    }
    return create_update.update_object(request, object_id=object_id, **kwargs)
    
@permission_required('bugwaz.status_report', Report)
@withproduct
def update_report_status(request, product, object_id):
    obj = get_object_or_404(Report, pk=object_id)
    if request.method == 'POST':
        form = ReportFormForStatus(request, request.POST, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.status == 'verified':
                action = 'verified'
            elif instance.status == 'resolved':
                action = 'resolved'
            else:
                action = 'status'
            instance.save(request, action=action)
            return redirect(instance)
    else:
        form = ReportFormForStatus(request, instance=obj)
    kwargs = {
        'template': r'bugwaz/report_form.html',
        'extra_context': {
            'product': product,
            'object': obj,
            'form': form,
        }
    }
    return simple.direct_to_template(request, **kwargs)
@permission_required('bugwaz.change_product', Product)
def update_product(request, object_id):
    kwargs = {
        'form_class': ProductForm,
    }
    return create_update.update_object(request, object_id=object_id, **kwargs)

@permission_required('bugwaz.delete_component', Component)
@withproduct
def delete_component(request, product, object_id):
    kwargs = {
        'model': Component,
        'post_delete_redirect': reverse('bugwaz-component-list', kwargs={'product': product.pk}),
        'extra_context': {
            'product': product,
        }
    }
    return create_update.delete_object(request, object_id=object_id, **kwargs)
@permission_required('bugwaz.delete_version', Version)
@withproduct
def delete_version(request, product, object_id):
    kwargs = {
        'model': Version,
        'post_delete_redirect': reverse('bugwaz-version-list', kwargs={'product': product.pk}),
        'extra_context': {
            'product': product,
        }
    }
    return create_update.delete_object(request, object_id=object_id, **kwargs)
@permission_required('bugwaz.delete_report', Report)
@withproduct
def delete_report(request, product, object_id):
    kwargs = {
        'model': Report,
        'post_delete_redirect': reverse('bugwaz-report-list', kwargs={'product': product.pk}),
        'extra_context': {
            'product': product,
        }
    }
    return create_update.delete_object(request, object_id=object_id, **kwargs)
@permission_required('bugwaz.delete_product', Product)
def delete_product(request, object_id):
    kwargs = {
        'model': Product,
        'post_delete_redirect': reverse('bugwaz-product-list'),
    }
    return create_update.delete_object(request, object_id=object_id, **kwargs)

#
# API
#----------------------------------------------------------------------------
@permission_required('bugwaz.charge_report', Report)
@withproduct
def charge_report(request, product, object_id):
    obj = get_object_or_404(Report, product=product, pk=object_id)
    obj.join(request.user)
    return redirect(obj)
@permission_required('bugwaz.charge_report', Report)
@withproduct
def discharge_report(request, product, object_id):
    obj = get_object_or_404(Report, product=product, pk=object_id)
    obj.quit(request.user)
    return redirect(obj)
