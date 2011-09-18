# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
# from snippets: http://djangosnippets.org/snippets/1071/
#
"""
Example usage:

    class ArticleView(RestView):
    
        def GET(request, article_id):
            return render_to_response("article.html", {
                'article': get_object_or_404(Article, pk = article_id),
            })

        def POST(request, article_id):
            # Example logic only; should be using django.forms instead
            article = get_object_or_404(Article, pk = article_id)
            article.headline = request.POST['new_headline']
            article.body = request.POST['new_body']
            article.save()
            return HttpResponseRedirect(request.path)

Then in your urls.py:

    from my_views import ArticleView
    
    urlpatterns = patterns('',
        ...
        (r'^article/(\d+)/$', ArticleView()),
        ...
    )

"""

from django.http import HttpResponse
import re

nonalpha_re = re.compile('[^A-Z]')

class RestView(object):
    """
    Subclass this and add GET / POST / etc methods.
    """
    allowed_methods = ('GET', 'PUT', 'POST', 'DELETE', 'HEAD', 'OPTIONS')
    
    def __call__(self, request, *args, **kwargs):
        method = nonalpha_re.sub('', request.method.upper())
        if not method in self.allowed_methods or not hasattr(self, method):
            return self.method_not_allowed(method)
        return getattr(self, method)(request, *args, **kwargs)
    
    def method_not_allowed(self, method):
        response = HttpResponse('Method not allowed: %s' % method)
        response.status_code = 405
        return response