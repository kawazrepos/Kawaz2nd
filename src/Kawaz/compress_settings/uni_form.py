# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'uni-form': {
        'source_filenames': (
            r'javascript/uni-form/css/uni-form.custom.css',
            r'javascript/uni-form/css/default.custom.uni-form.css',
        ),
        'output_filename': r'css/compressed/uni-form.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {
    'uni-form': {
        'source_filenames': (
            r'javascript/uni-form/uni-form.jquery.js',
        ),
        'output_filename': r'javascript/compressed/uni-form.js',
    },
}