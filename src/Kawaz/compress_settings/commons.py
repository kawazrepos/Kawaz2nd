# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'commons-material-base': {
        'source_filenames': (
            r"css/views/commons/overview-summary.css",
            r"css/views/projects/overview-summary.css",
        ),
        'output_filename': r'css/compressed/commons-material-base.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'commons-material-detail': {
        'source_filenames': (
            r"css/views/commons/material-detail.css",
        ),
        'output_filename': r'css/compressed/commons-material-detail.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'commons-material-list': {
        'source_filenames': (
            r"css/views/commons/material-list.css",
            r"css/views/profiles/overview-summary.css",
            r"css/views/projects/overview-summary.css",
        ),
        'output_filename': r'css/compressed/commons-material-list.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {}