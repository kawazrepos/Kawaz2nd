# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'index-authenticated': {
        'source_filenames': (
            r'css/views/index/authenticated.css',
            r'css/views/profiles/overview-summary.css',
            r'css/views/history/timeline-list.css',
            r'css/views/tweets/tweet-base.css',
            r'css/views/tweets/tweet-list.css',
            r'css/views/events/event-list.css',
            r'css/views/comments/comment-list-tiny.css',
            r'css/views/projects/project-list.css',
        ),
        'output_filename': r'css/compressed/index-authenticated.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {
    'index-authenticated': {
        'source_filenames': (
            r'javascript/components/profile-mood-editable.js',
            r'javascript/components/tweets-tweet.js',
        ),
        'output_filename': r'javascript/compressed/index-authenticated.js',
    },
}