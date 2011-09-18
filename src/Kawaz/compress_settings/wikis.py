# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/04
#
COMPRESS_CSS = {
    'wikis-entry-base': {
        'source_filenames': (
            r'css/views/projects/overview-summary.css',
        ),
        'output_filename': r'css/compressed/wikis-entry-base.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS= {}