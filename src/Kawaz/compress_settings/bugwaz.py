# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'bugwaz-product-detail': {
        'source_filenames': (
            r"css/views/bugwaz/report-list.css",
            r"css/views/bugwaz/product-detail.css",
        ),
        'output_filename': r'css/compressed/bugwaz-product-detail.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'bugwaz-report-base': {
        'source_filenames': (
            r"css/views/bugwaz/report-overview-summary.css",
        ),
        'output_filename': r'css/compressed/bugwaz-report-base.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'bugwaz-component-detail': {
        'source_filenames': (
            r"css/views/bugwaz/report-list.css",
        ),
        'output_filename': r'css/compressed/bugwaz-component-detail.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'bugwaz-version-detail': {
        'source_filenames': (
            r"css/views/bugwaz/report-list.css",
        ),
        'output_filename': r'css/compressed/bugwaz-version-detail.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'bugwaz-report-list': {
        'source_filenames': (
            r"css/views/bugwaz/report-list.css",
        ),
        'output_filename': r'css/compressed/bugwaz-report-list.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {}