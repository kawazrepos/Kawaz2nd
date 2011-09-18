# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'history-timeline-list': {
        'source_filenames': (
            r'css/views/history/timeline-list.css',
        ),
        'output_filename': r'css/compressed/history-timeline-list.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {}