# -*- coding: utf-8 -*-

from libwaz import forms

from models import Project, Category

class GroupedSelectWidget(forms.widgets.Select):
    def __init__(self, *args, **kwargs):
        choices = []
        parents = Category.objects.filter(parent=None)
        for parent in parents:
            group = [parent.label]
            elements = []
            for child in parent.children.all():
                elements.append((child.pk, child.label))
            group.append(elements) 
            choices.append(group)
        super(GroupedSelectWidget, self).__init__(*args, choices=choices, **kwargs)

class ProjectForm(forms.ModelFormWithRequest):
    class Meta:
        model = Project
        fields = (
            'pub_state', 'slug', 'title', 
            'status', 'permission', 'icon', 'body',
            'category',
        )
        widgets = {
            'category': GroupedSelectWidget()
        }
        
class ProjectUpdateForm(ProjectForm):
    #
    # Notice:
    #   `slug`は変更不可能フィールドなので更新用フォームでは表示しない
    class Meta:
        model = Project
        fields = (
            'pub_state', 'title', 
            'status', 'permission', 'icon', 'body',
            'category',
        )