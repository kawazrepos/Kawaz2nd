# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
COMPRESS_CSS = {
    'components': {
        'source_filenames': (
            r'css/components/scrollto.css',
            r'css/components/ctimg.css',
            r'css/components/mtimg.css',
            r'css/components/hlist.css',
            r'css/components/ilist.css',
            r'css/components/fenced.css',
            r'css/components/pagination.css',
            r'css/components/markdown.css',
            r'css/components/filterset.css',
            r'css/colorbox/colorbox.css',
            #r'css/plugins/jquery.fancybox.css',
        ),
        'output_filename': r'css/compressed/components.css',
        'extra_context': {
            'media': 'screen, projection, print',
        },
    },
    'jquery-ui':{
        'source_filenames': (
            r'css/jquery-ui/pepper-grinder/jquery-ui-1.8.5.custom.css',
            r'css/jquery-ui/jquery-ui-timepicker-addon-0.6.css',
        ),
        'output_filename': r'css/compressed/jquery-ui.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
    'syntaxhighlighter':{
        'source_filenames': (
            r'javascript/syntaxhighlighter/styles/shCore.css',
            r'javascript/syntaxhighlighter/styles/shThemeDefault.css',
        ),
        'output_filename': r'css/compressed/syntaxhighlighter.css',
        'extra_context': {
            'media': 'screen, projection, print',
        }
    },
    'layouts': {
        'source_filenames': (
            r'css/layouts/form.css',
            r'css/layouts/common.css',
            r'css/layouts/messages.css',
            r'css/layouts/calls.css',
            r'css/layouts/authentification.css',
            r'css/layouts/header.css',
            r'css/layouts/advertisement.css',
            r'css/layouts/breadcrumbs.css',
            r'css/layouts/navigation.css',
            r'css/layouts/overview.css',
            r'css/layouts/content.css',
            r'css/layouts/action.css',
            r'css/layouts/footer.css',
            r'css/layouts/preview.css',
        ),
        'output_filename': r'css/compressed/layouts.css',
        'extra_context': {
            'media': 'screen, projection',
        }
    },
}
COMPRESS_JS = {
    'components': {
        'source_filenames': (
            r'javascript/jquery-1.4.4.js',
            r'javascript/plugins/jquery.json.js',
            r'javascript/plugins/jquery.cookie.js',
            r'javascript/plugins/jquery.lightbox_me.js',
            r'javascript/plugins/jquery.colorbox.js',
            #r'javascript/plugins/jquery.fancybox.js',
            r'javascript/plugins/jquery.qtip.min.js',
            r'javascript/components/messages.js',
            r'javascript/components/buttons.js',
            r'javascript/components/initialize.js',
            r'javascript/components/postlink.js',
            r'javascript/components/thread-anchorpopup.js',
            r'javascript/components/advertisement.js',
        ),
        'output_filename': r'javascript/compressed/components.js',
    },
    'jquery-ui': {
        'source_filenames': (
            r'javascript/jquery-ui-1.8.5.full.min.js',
            r'javascript/plugins/jquery-ui-timepicker-addon-0.6.js',
        ),
        'output_filename': r'javascript/compressed/jquery-ui.js',
    },
    'syntaxhighlighter': {
        'source_filenames': (
            r'javascript/syntaxhighlighter/scripts/shCore.js',
            r'javascript/syntaxhighlighter/scripts/shBrushBash.js',
            r'javascript/syntaxhighlighter/scripts/shBrushCSharp.js',
            r'javascript/syntaxhighlighter/scripts/shBrushCpp.js',
            r'javascript/syntaxhighlighter/scripts/shBrushCss.js',
            r'javascript/syntaxhighlighter/scripts/shBrushJScript.js',
            r'javascript/syntaxhighlighter/scripts/shBrushJava.js',
            r'javascript/syntaxhighlighter/scripts/shBrushPerl.js',
            r'javascript/syntaxhighlighter/scripts/shBrushPhp.js',
            r'javascript/syntaxhighlighter/scripts/shBrushPlain.js',
            r'javascript/syntaxhighlighter/scripts/shBrushPython.js',
            r'javascript/syntaxhighlighter/scripts/shBrushRuby.js',
            r'javascript/syntaxhighlighter/scripts/shBrushScala.js',
            r'javascript/syntaxhighlighter/scripts/shBrushSql.js',
            r'javascript/syntaxhighlighter/scripts/shBrushVb.js',
            r'javascript/syntaxhighlighter/scripts/shBrushXml.js',
        ),
        'output_filename': r'javascript/compressed/syntaxhighlighter.js',
    },
}