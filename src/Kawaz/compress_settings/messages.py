# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/29
#
COMPRESS_CSS = {
    'messages-message-inbox': {
        'source_filenames': (
            r"css/views/messages/message-inbox.css",
        ),
        'output_filename': r'css/compressed/messages-message-inbox.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    }
}
COMPRESS_JS = {
}