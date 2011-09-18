# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'events-event-list': {
        'source_filenames': (
            r'css/views/events/event-list.css',
            r'css/views/comments/comment-list-tiny.css',
        ),
        'output_filename': r'css/compressed/events-event-list.css',
        'extra_context': {
            'media': 'screen, projection, print',
        },
    },
    'events-event-detail': {
        'source_filenames': (
            r'css/views/events/event-detail.css',
        ),
        'output_filename': r'css/compressed/events-event-detail.css',
        'extra_context': {
            'media': 'screen, projection, print',
        },
    },
}
COMPRESS_JS = {}