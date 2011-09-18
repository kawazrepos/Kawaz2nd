# -*- coding: utf-8 -*-
#
# Created:        2010/11/08
# Author:        alisue
#
from django import forms
from django.utils.translation import ugettext as _
from django.core.urlresolvers import resolve, Resolver404
from django.contrib.auth.models import User
from urlparse import urlparse

from registration.forms import RegistrationForm as _RegistrationForm
from models import RegistrationProfile

attrs_dict = {'class': 'required'}

class RegistrationForm(_RegistrationForm):
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")},
                                help_text=_('This is used for your login name so DO NOT forget it'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("Email address"),
                             help_text=_('This is used for contact with you so please use email address for your daily use.'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"))
    remarks = forms.CharField(label=_('Remarks'), widget=forms.Textarea(), required=True,
                              help_text=_('Please input motives and district where you live otherwise your registration will kicked out.'))
    
    def clean_username(self):
        username = super(RegistrationForm, self).clean_username()
        try: resolve(urlparse('/' + username + '/')[2])
        except Resolver404:
            return username

        raise forms.ValidationError(_('This username conflict with exists URL. Please chose another.'))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('This email is already registered. Please chose another.'))
        return email
    
    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    
    """
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={'required': _("You must agree to the terms to register")})

class RegistrationHandleForm(forms.Form):
    ACTIONS = (
        ('approve', _('Approve')),
        ('reject',  _('Reject')),
    )
    registration_profiles   = forms.ModelMultipleChoiceField(label=_('registration profiles'), queryset=RegistrationProfile.objects.filter(status='waiting'))
    action                  = forms.ChoiceField(label=_('Action'), choices=ACTIONS)

class CSVRegistrationForm(forms.Form):
    csv_file    = forms.FileField(label=_('csv file'))