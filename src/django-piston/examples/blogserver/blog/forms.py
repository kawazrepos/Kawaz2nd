from django.forms import ModelForm

from blogserver.blog.models import Blogpost

class BlogpostForm(ModelForm):
    class Meta:
        model = Blogpost
        exclude = ('author',)