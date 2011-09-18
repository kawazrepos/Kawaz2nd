# -*- coding: utf-8 -*-
from libwaz import forms
from django.core.exceptions import ValidationError

from ..projects.models import Project
from ..profiles.models import Profile
from models import Task

class TaskForm(forms.ModelFormWithRequest):
    class Meta:
        model = Task
        fields = (
            'project',
            'pub_state',
            'title', 'body',
            'priority',
            'deadline',
            'owners',
        )
    
    def __init__(self, request, *args, **kwargs):
        super(TaskForm, self).__init__(request, *args, **kwargs)
        if kwargs.get('initial') and 'project' in kwargs['initial']:
            project = Project.objects.get(pk=kwargs['initial']['project'])
            self.fields['project'].widget = forms.HiddenInput()
            self.fields['owners'].choices = [(user.pk, user.get_profile().nickname) for user in project.members.all()]
        else:
            self.fields['project'].queryset = request.user.projects_joined.all()
            # JavaScriptで選択されているプロジェクトメンバーのみ表示するように書いてあるので以下でおｋ
            self.fields['owners'].choices = [(profile.user.pk, profile.nickname) for profile in Profile.objects.published(request)]
    
    def validate_unique(self):
        #
        # Notice:
        #    `unique_together`のチェックを行うために除外した`author`を含めて
        #    validate_uniqueを呼び出す
        #
        exclude = self._get_validation_exclusions()
        exclude.remove('author')
    
        try:
            self.instance.validate_unique(request=self.request, exclude=exclude)
        except ValidationError, e:
            self._update_errors(e.message_dict)