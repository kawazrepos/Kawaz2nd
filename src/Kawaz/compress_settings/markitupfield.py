# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'markitupfield': {
        'source_filenames': (
            r"css/plugins/django.commons.css",
            r"javascript/markitup/sets/markdown-extra/style.css",
            r"javascript/markitup/skins/simple/style.css",
        ),
        'output_filename': r'css/compressed/markitupfield.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    }
}
COMPRESS_JS = {
    'markitupfield': {
        'source_filenames': (
            r'javascript/markitup/jquery.markitup.js',
            r'javascript/markitup/sets/markdown-extra/set.js',
            r'javascript/plugins/jquery.upload-1.0.2.js',
            r'javascript/django/django.commons.js',
            r'javascript/plugins/jquery.markitup.indent.js',
            r'javascript/plugins/jquery.markitup.fullscreen.js',
            r'javascript/django/django.markitupfield.js',
        ),
        'output_filename': r'javascript/compressed/markupfield.js',
    },
}