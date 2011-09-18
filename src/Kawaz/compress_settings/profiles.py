# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'profiles-profile-list': {
        'source_filenames': (
            r'css/views/profiles/profile-list.css',
        ),
        'output_filename': r'css/compressed/profiles-profile-list.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'profiles-profile-detail': {
        'source_filenames': (
            r'css/views/profiles/overview-summary.css',
            r'css/views/profiles/profile-detail.css',
        ),
        'output_filename': r'css/compressed/profiles-profile-detail.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'profiles-profile-form': {
        'source_filenames': (
            r'css/plugins/jquery.image-dropdown.css',
            r'css/views/profiles/profile-form.css',
        ),
        'output_filename': r'css/compressed/profiles-profile-form.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {
    'profiles-profile-detail': {
        'source_filenames': (
            r'javascript/components/profile-mood-editable.js',
        ),
        'output_filename': r'javascript/compressed/profiles-profile-detail.js',
    },
    'profiles-profile-form': {
        'source_filenames': (
            # 要注意
            r'javascript/plugins/jquery.formset.min.js',
            r'javascript/plugins/jquery.image-dropdown.js',
            r'javascript/components/profiles-profile-form.js',
        ),
        'output_filename': r'javascript/compressed/profiles-profile-form.js',
    },
}