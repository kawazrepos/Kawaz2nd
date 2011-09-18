from django.core.urlresolvers import reverse

from models import MarkItUpComment
from forms import MarkItUpCommentForm

def get_model():
    return MarkItUpComment

def get_form():
    return MarkItUpCommentForm

def get_delete_url(comment):
    return reverse('mcomment-comment-delete', kwargs={'object_id': comment.pk})