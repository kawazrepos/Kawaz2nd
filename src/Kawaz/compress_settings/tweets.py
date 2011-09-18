COMPRESS_CSS = {
    'tweets-tweet-base': {
        'source_filenames': (
            r'css/views/tweets/tweet-base.css',
            r'css/views/tweets/tweet-list.css',
        ),
        'output_filename': r'css/compressed/tweets-tweet-base.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {
    'tweets-tweet-base': {
        'source_filenames': (
            r'javascript/components/tweets-tweet.js',
        ),
        'output_filename': r'javascript/compressed/tweets-tweet-base.js',
    },
}