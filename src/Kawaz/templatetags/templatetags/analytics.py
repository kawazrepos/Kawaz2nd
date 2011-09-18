# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
# from snippets: http://djangosnippets.org/snippets/457/
#
from django import template

register = template.Library()

def urchin(uacct):
    return """
<script src="http://www.google-analytics.com/urchin.js" type="text/javascript">
</script>
<script type="text/javascript">
_uacct = "%(uacct)s";
urchinTracker();
</script>
""" % { 'uacct': uacct }

register.simple_tag(urchin)