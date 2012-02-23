from django.dispatch import Signal
from registration.signals import user_registered
from registration.signals import user_activated

user_accepted = Signal(providing_args=['user', 'request'])
user_rejected = Signal(providing_args=['user', 'request', 'reason'])
