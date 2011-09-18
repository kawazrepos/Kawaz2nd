# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'blogs-entry-base': {
        'source_filenames': (
            r'css/views/blogs/entry-base.css',
            r'css/views/profiles/overview-summary.css',
        ),
        'output_filename': r'css/compressed/blogs-entry-base.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'blogs-entry-form': {
        'source_filenames': (
            r'css/plugins/jquery.appendable.css',
        ),
        'output_filename': r'css/compressed/blogs-entry-form.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {
    'blogs-entry-form': {
        'source_filenames': (
            r'javascript/plugins/jquery.appendable.js',
        ),
        'output_filename': r'javascript/compressed/blogs-entry-form.js',
    },
}