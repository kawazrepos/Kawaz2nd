from django.conf import settings

settings.RESAVE_WHITE_LIST = getattr(settings, 'RESAVE_WHITE_LIST', None)
settings.RESAVE_BLACK_LIST = getattr(settings, 'RESAVE_BLACK_LIST', (
    'auth.user',
    'auth.group',
    'auth.permission',
    'auth.message',
    'contenttypes.contenttype',
    'sessions.session',
    'sites.site',
    'admin.logentry',
    'comments.comment',
    'comments.commentflag',
    'flatpages.flatpage',
))