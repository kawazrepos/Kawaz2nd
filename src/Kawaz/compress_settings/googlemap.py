# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/29
#
COMPRESS_CSS = { 
}
COMPRESS_JS = {
    'googlemap': {
        'source_filenames': (
            r'javascript/django/django.googlemap.js',
        ),
        'output_filename': r'javascript/compressed/googlemap.js',
    },
}