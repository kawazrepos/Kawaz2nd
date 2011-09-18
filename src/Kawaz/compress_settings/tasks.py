# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/04
#
COMPRESS_CSS = {
    'tasks-task-base': {
        'source_filenames': (
            r'css/views/projects/overview-summary.css',
            r'css/views/tasks/overview-summary.css',
        ),
        'output_filename': r'css/compressed/tasks-task-base.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'tasks-task-list': {
        'source_filenames': (
            r'css/views/tasks/task-list.css',
        ),
        'output_filename': r'css/compressed/tasks-task-list.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {
}