# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/25
#
from libwaz import forms
import models

class ComponentForm(forms.ModelForm):
    class Meta:
        model = models.Component
        widgets = {
            'product':  forms.HiddenInput,
        }
class VersionForm(forms.ModelForm):
    class Meta:
        model = models.Version
        widgets = {
            'product':  forms.HiddenInput,
        }
class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = (
            'label', 'body', 'rules', 'group',
        )
        widgets = {
            'group':    forms.HiddenInput,
        }
class ReportForm(forms.ModelFormWithRequest):
    class Meta:
        model = models.Report
        fields = (
            'username', 'label', 'body',
            'component', 'version', 'serverity', 'os',
            'product',
        )
        widgets = {
            'product': forms.HiddenInput,
            'username': forms.HiddenInput
        }
class ReportFormForAnonymous(forms.ModelFormWithRequest):
    class Meta:
        model = models.Report
        fields = (
            'username', 'label', 'body',
            'component', 'version', 'serverity', 'os',
            'product',
        )
        widgets = {
            'product': forms.HiddenInput,
        }
class ReportFormForStatus(forms.ModelFormWithRequest):
    class Meta:
        model = models.Report
        fields = (
            'status', 'resolution', 'priority',
            'product',
        )
        widgets = {
            'product': forms.HiddenInput,
        }