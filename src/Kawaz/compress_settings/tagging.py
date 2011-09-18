# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'tagging': {
        'source_filenames': (
            r'css/plugins/jquery.contextMenu.css',
            r'css/plugins/django.tagging.css',
        ),
        'output_filename': r'css/compressed/tagging.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {
    'tagging': {
        'source_filenames': (
            # 要注意
            r'javascript/plugins/jquery.contextMenu.js',
            r'javascript/django/django.tagging.js',
        ),
        'output_filename': r'javascript/compressed/tagging.js',
    },
}