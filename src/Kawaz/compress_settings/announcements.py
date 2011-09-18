# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'announcements-announcement-detail': {
        'source_filenames': (
            r'css/views/announcements/announcenemt-detail.css',
        ),
        'output_filename': r'css/compressed/announcements-announcement-detail.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {}