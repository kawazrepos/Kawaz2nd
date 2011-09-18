# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/18
#
from django import template
from django.conf import settings

register = template.Library()

@register.filter("urlize_html")
def urlize_html(html):
    """
    Returns urls found in an (X)HTML text node element as urls via Django urlize filter.
    """
    try:
        from BeautifulSoup import BeautifulSoup
        from django.utils.html import urlize
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError, "Error in urlize_html The Python BeautifulSoup libraries aren't installed."
        return html
    else:
        soup = BeautifulSoup(html)
           
        textNodes = soup.findAll(text=True)
        for textNode in textNodes:
            urlizedText = urlize(textNode)
            textNode.replaceWith(urlizedText)
            
        return str(soup)
