# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'threads-thread-base': {
        'source_filenames': (
            r'css/views/threads/thread-base.css',
            r'css/views/projects/overview-summary.css',
        ),
        'output_filename': r'css/compressed/threads-thread-base.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'threads-thread-list': {
        'source_filenames': (
            r'css/views/threads/thread-list.css',
        ),
        'output_filename': r'css/compressed/threads-thread-list.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'threads-thread-detail': {
        'source_filenames': (
            r'css/views/threads/thread-detail.css',
        ),
        'output_filename': r'css/compressed/threads-thread-detail.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {}