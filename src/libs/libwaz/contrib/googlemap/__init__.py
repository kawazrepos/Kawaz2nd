from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if not hasattr(settings, 'GOOGLEMAP_API_URL') and not hasattr(settings, 'GOOGLEMAP_API_SENSOR'):
    raise ImproperlyConfigured("You must define the GOOGLEMAP_API_SENSOR setting before using the field.")
if not hasattr(settings, 'GOOGLEMAP_SCRIPT_URL'):
    raise ImproperlyConfigured("You must define the GOOGLEMAP_API_URL setting before using the field.")

# Google Map
settings.GOOGLEMAP_API_URL = getattr(settings, 'GOOGLEMAP_API_URL', r'http://maps.google.com/maps/api/js?sensor=%(sensor)s')
settings.GOOGLEMAP_SENSOR = getattr(settings, 'GOOGLEMAP_API_SENSOR')
# GoogleMapField
settings.GOOGLEMAP_SCRIPT_URL = getattr(settings, 'GOOGLEMAP_SCRIPT_URL')
settings.GOOGLEMAP_CLASS_NAME = getattr(settings, 'GOOGLEMAP_CLASS_NAME', 'django-googlemap-surface')

# Default values
from decimal import Decimal
settings.GOOGLEMAP_DEFAULT_LATITUDE = getattr(settings, 'GOOGLEMAP_DEFAULT_LATITUDE', Decimal("43.068625"))
settings.GOOGLEMAP_DEFAULT_LONGITUDE = getattr(settings, 'GOOGLEMAP_DEFAULT_LONGITUDE', Decimal("141.350801"))
settings.GOOGLEMAP_DEFAULT_ZOOM = getattr(settings, 'GOOGLEMAP_DEFAULT_ZOOM', 15)

