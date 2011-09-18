# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/30
#

# Append Kawaz to the PYTHONPATH
import os, sys
path_list = [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'Kawaz'),
    os.path.join(os.path.dirname(__file__), 'libs'),
]
for path in path_list:
    if path not in sys.path:
        sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Kawaz.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
