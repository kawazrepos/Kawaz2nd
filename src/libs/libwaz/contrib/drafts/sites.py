# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/11
#
from django.db.models.base import ModelBase

from exceptions import AlreadyRegistered, NotRegistered

class DraftSite(object):
    def __init__(self):
        self._registry = {}
    
    def register(self, model, backend_class=None):
        """
        Registers a model with the site.
        
        The model should be a Model class, not instances.
        
        If no custom backend is provided, a generic Backend will be applied
        to the model.
        """
        if not backend_class:
            from backends import BasicDraftBackend
            backend_class = BasicDraftBackend
        
        if not isinstance(model, ModelBase):
            raise AttributeError('The model being registered must derive from Model.')
        
        if model in self._registry:
            raise AlreadyRegistered('The model %s is already registered' % model.__class__)
        
        self._registry[model] = backend_class()
        self._setup(model, self._registry[model])
    
    def unregister(self, model):
        """
        Unregisters a model from the site.
        """
        if model not in self._registry:
            raise NotRegistered('The model %s is not registered' % model.__class__)
        self._teardown(model, self._registry[model])
        del(self._registry[model])
    
    def _setup(self, model, backend):
        backend.setUp(model)
    
    def _teardown(self, model, backend):
        backend.tearDown(model)
    
    def get_backend(self, model):
        """Provide the backend that're being used for a particular model."""
        if model not in self._registry:
            raise NotRegistered('The model %s is not registered in %s' % (model.__class__, self._registry))
        return self._registry[model]
    
    def get_backends(self):
        """Provide a dict of all backends that're being used."""
        return self._registry
    
site = DraftSite()