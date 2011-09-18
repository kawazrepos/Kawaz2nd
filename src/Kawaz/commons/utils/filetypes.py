# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/28
#
import mimetypes

IMAGE = (
    'image/bmp',
    'image/x-ms-bmp',
    'image/jpeg',
    'image/png',
    'image/gif',
)
AUDIO = (
    'audio/midi',
    'audio/mpeg',
    'audio/x-wav',
    'application/x-ogg',
)
MOVIE = (
    'video/mp4',
    'video/mpeg',
    'video/x-ms-wmv',
    'video/x-msvideo',
    'video/x-flv',
)
ARCHIVE = (
    'application/x-bzip2',
    'application/x-gtar',
    'application/x-gzip',
    'application/x-lzh',
    'application/x-tar',
    'application/zip',
)
TEXT = (
    'application/atom+xml',
    'application/msword',
    'application/pdf',
    'application/rdf+xml',
    'application/rss+xml',
    'application/x-latex',
    'application/x-tex',
    'application/xhtml+xml',
    'text/css',
    'text/html',
    'text/plain',
    'text/richtext',
    'text/rtf',
    'text/x-scalar',
    'text/x-cpp',
    'text/x-csharp',
    'text/x-ruby',
    'text/x-perl',
    'text/x-python',
    'application/x-wais-source'
)
APPLICATION = (
    'application/octet-stream',
    'application/x-csh',
    'application/x-httpd-cgi',
    'application/x-javascript',
    'application/x-sh',
)
TYPES = (
    ('image',       IMAGE),
    ('audio',       AUDIO),
    ('movie',       MOVIE),
    ('text',        TEXT),
    ('archive',     ARCHIVE),
    ('application', APPLICATION),
)
def guess(filename):
    mimetypes.init()
    try:
        type = mimetypes.guess_type(filename)[0]
    except:
        # Fail silently
        type = None
    if type is None:
        return 'unknown'
    for label, types in TYPES:
        if type in types:
            return label
    return 'unknown'
