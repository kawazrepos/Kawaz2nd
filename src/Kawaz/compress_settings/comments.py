# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'comments': {
        'source_filenames': (
            r"css/views/comments/comment-list.css",
            r"css/views/comments/comment-form.css",
        ),
        'output_filename': r'css/compressed/comments.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {}