# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'search': {
        'source_filenames': (
            r'css/components/search.css',
        ),
        'output_filename': r'css/compressed/search.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {}