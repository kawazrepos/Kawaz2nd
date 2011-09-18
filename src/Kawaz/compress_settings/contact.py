# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/13
#
# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'contact-email-form': {
        'source_filenames': (
            r"css/views/contact/email-form.css",
        ),
        'output_filename': r'css/compressed/contact-email-form.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {}