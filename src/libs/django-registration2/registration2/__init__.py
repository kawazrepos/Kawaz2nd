from django.conf import settings

# registration2 required registration
if 'registration' not in settings.INSTALLED_APPS:
    settings.INSTALLED_APPS.append('registration')
