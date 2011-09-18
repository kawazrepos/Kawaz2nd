# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/13
#
COMPRESS_CSS = {
    'flatpages-flatpage-list': {
        'source_filenames': (
            r'css/views/flatpages/flatpage-list.css',
        ),
        'output_filename': r'css/compressed/flatpages-flatpage-list.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {}