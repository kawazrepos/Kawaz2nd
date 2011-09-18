# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
# Warning:
#    ここはデザイン実験などで一時的に compressed を使用するための場所です
#    したがってここに書かれた内容は開発バージョンでは読み込まれますが製品
#    では読み込まれないので注意してください
#
# Example
#    COMPRESS_CSS = {
#        'components': {
#            'source_filenames': (
#                r'css/components/ctimg.css',
#                r'css/components/mtimg.css',
#                r'css/components/hlist.css',
#                r'css/components/ilist.css',
#                r'css/components/fenced.css',
#                r'css/components/pagination.css',
#                r'css/components/markdown.css',
#            ),
#            'output_filename': r'css/compressed/components.css',
#            'extra_context': {
#                'media': 'screen, projection, print',
#            },
#        },
#    }
#    COMPRESS_JS = {
#        'common': {
#            'source_filenames': (
#                r'javascript/jquery-1.4.2.js',
#                r'javascript/plugins/jquery.json.js',
#                r'javascript/plugins/jquery.cookie.js',
#                r'javascript/components/messages.js',
#                r'javascript/plugins/jquery.lightbox_me.js',
#            ),
#            'output_filename': r'javascript/compressed/common.js',
#        },
#    }
#
COMPRESS_CSS = {}
COMPRESS_JS = {}