# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'projects-project-base': {
        'source_filenames': (
            r'css/views/projects/overview-summary.css',
            r'css/views/projects/project-base.css',
        ),
        'output_filename': r'css/compressed/projects-project-base.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'projects-project-detail': {
        'source_filenames': (
            r'css/views/projects/project-detail.css',
        ),
        'output_filename': r'css/compressed/projects-project-detail.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'projects-project-list': {
        'source_filenames': (
            r'css/views/projects/project-list.css',
        ),
        'output_filename': r'css/compressed/projects-project-list.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {}