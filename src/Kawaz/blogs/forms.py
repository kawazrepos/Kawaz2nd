# -*- coding: utf-8 -*-
#
# Created:    2010/09/10
# Author:         alisue
#
from django.core.exceptions import ValidationError

from models import Category, Entry

from libwaz.forms import ModelFormWithRequest

class CategoryForm(ModelFormWithRequest):
    class Meta:
        model = Category
        
class EntryForm(ModelFormWithRequest):
    class Meta:
        model = Entry
        fields = ('pub_state', 'title', 'body', 'category')
    
    def __init__(self, request, *args, **kwargs):
        super(EntryForm, self).__init__(request, *args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(author=request.user)
    
    def validate_unique(self):
        #
        # Notice:
        #    `unique_together`のチェックを行うために除外した`author`を含めて
        #    validate_uniqueを呼び出す
        #
        exclude = self._get_validation_exclusions()
        exclude.remove('author')
        exclude.remove('publish_at_date')
    
        try:
            self.instance.validate_unique(request=self.request, exclude=exclude)
        except ValidationError, e:
            self._update_errors(e.message_dict)