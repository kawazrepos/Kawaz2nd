from django.db.models import get_models
from django.db.models.signals import post_syncdb
from django.utils.encoding import smart_unicode

from django.contrib.auth.management import create_permissions, _get_all_permissions

# Hack the postsyncdb signal, so we can fix the misbehavior of the
# content_type
# assignment to the proxy models.
# see http://code.djangoproject.com/ticket/11154

def create_permissions_respecting_proxy(
    app, created_models, verbosity, **kwargs
    ):

    if not kwargs['sender'].__name__ == 'customer.models':
        # if not in 'customer' app, then use the original function
        create_permissions(app, created_models, verbosity, **kwargs)
        return

    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth import models as auth_app
    app_models = get_models(app)
    searched_perms = list()
    ctypes = set()
    for klass in app_models:
        # this is where the difference is: the original create_permissions
        # use ctype = ContentType.objects.get_for_model(klass)
        opts = klass._meta
        ctype, created = ContentType.objects.get_or_create(
            app_label=opts.app_label,
            model=opts.object_name.lower(),
            defaults = {'name': smart_unicode(opts.verbose_name_raw)}
            )
        # end of the modification
        ctypes.add(ctype)
        for perm in _get_all_permissions(klass._meta):
            searched_perms.append((ctype, perm))

    all_perms = set(auth_app.Permission.objects.filter(
            content_type__in=ctypes
            ).values_list("content_type", "codename"))

    for ctype, (codename, name) in searched_perms:
        if(ctype.pk, codename) in all_perms:
            continue
        p = auth_app.Permission.objects.create(
            codename=codename, name=name, content_type=ctype
            )
        if verbosity >=2:
            print "Adding permission '%s'" % p

post_syncdb.disconnect(
    create_permissions,
    dispatch_uid='django.contrib.auth.management.create_permissions',
    )

post_syncdb.connect(
    create_permissions_respecting_proxy,
    dispatch_uid='django.contrib.auth.management.create_permissions',
    )

