# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/03
#
from django.db.models.loading import get_models
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ImproperlyConfigured

from ...utils import resave

class Command(BaseCommand):
    help = u"Resave objects of each model."

    def handle(self, *app_labels, **options):
        from django.db import models
        if not app_labels:
            output = [self.handle_noargs(**options)]
        else:
            try:
                app_list = [models.get_app(app_label) for app_label in app_labels]
            except (ImproperlyConfigured, ImportError), e:
                raise CommandError("%s. Are you sure your INSTALLED_APPS setting is correct?" % e)
            output = []
            for app in app_list:
                app_output = self.handle_app(app, **options)
                if app_output:
                    output.append(app_output)
        return '\n'.join(output)
    
    def handle_app(self, app, **options):
        output = []
        model_list = get_models(app)
        for model in model_list:
            _output = self._handle_model(model, **options)
            if _output:
                output.append(_output)
        return "\n".join(output)
    
    def handle_noargs(self, **options):
        output = []
        model_list = resave._model_list()
        for model in model_list:
            _output = self._handle_model(model, **options)
            if _output:
                output.append(_output)
        return "\n".join(output)
    
    def _handle_model(self, model, **options):
        count = resave.resave(model)
        if options['verbosity'] != 0:
            if count or options['verbosity'] == '2':
                return "%s: %d object is saved." % (model, count)
        return ''