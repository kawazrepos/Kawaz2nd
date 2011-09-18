# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
# from snippets: http://djangosnippets.org/snippets/45/
#
from django import template
from django.conf import settings

register = template.Library()

@register.filter
def getlinks(value):
    """
    Returns links found in an (X)HTML string as Python objects for itteration in templates.
    
    EXAMPLE:
    
    <ul>
      {% for link in blog.entry.body|getlinks %}
         <li><a href="{{ link.href }}">{{ link.title }}</a></li>
      {% endfor %}
    </ul>
    
    """
    try:
        import beautifulsoup
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError, "Error in {% getlinks %} filter: The Python BeautifulSoup and/or urllib2 libraries aren't installed."
        return value
    else:
        soup = beautifulsoup.BeautifulSoup(value)
        return soup.findAll('a')
