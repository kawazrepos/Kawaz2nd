# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from models import Draft

BODY_ATTRS = (
    'body',
    '__unicode__',
)
class BaseDraftBackend(object):
    def setUp(self, model):
        pass
    def tearDown(self, model):
        pass
    def autodiscover(self, instance, url=None, label=None, body=None, created_at=None, updated_at=None):
        raise NotImplementedError
    
    def autodiscovers(self, model, request):
        if hasattr(model.objects, 'draft'):
            qs = model.objects.draft(request)
        else:
            qs = model.objects.filter(pub_state='draft', author=request.user)
        for instance in qs.all():
            yield self.autodiscover(instance)

class BasicDraftBackend(BaseDraftBackend):
    def _get_url(self, instance):
        return instance.get_absolute_url()
    def _get_label(self, instance):
        return instance.__unicode__()
    def _get_body(self, instance):
        body = None
        for attr in BODY_ATTRS:
            body = getattr(instance, attr, None)
            if body: break
        if callable(body): body = body()
        if body is None: body = ''
        return body
    def _get_created_at(self, instance):
        return instance.created_at
    def _get_updated_at(self, instance):
        return instance.updated_at
    
    def autodiscover(self, instance, url=None, label=None, body=None, created_at=None, updated_at=None):
        if url is None:
            url = self._get_url(instance)
        if label is None:
            label = self._get_label(instance)
        if body is None:
            body = self._get_body(instance)
        if created_at is None:
            created_at = self._get_created_at(instance)
        if updated_at is None:
            updated_at = self._get_updated_at(instance)
        draft = Draft(
            instance=instance,
            url=url,
            label=label,
            body=body,
            created_at=created_at,
            updated_at=updated_at,
        )
        return draft