# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2011/01/17
#
import csv
from backends import get_backend
from models import RegistrationProfile

def mkpasswd(length=8, digit=True, lower=True, upper=True):
    from random import choice
    DIGIT = "0123456789"
    LOWER = "abcdefghijkmnopqrstuvwxyz"     # Except 'l'
    UPPER = "ABCDEFGHIJKLMNPQRSTUVWXYZ"     # Except 'O'
    seed = ""
    if digit:
        seed += DIGIT
    if lower:
        seed += LOWER
    if upper:
        seed += UPPER
    return "".join([choice(seed) for i in range(length)])

def register_from_csv(request, backend, file):
    # Notice:
    #    DO NOT CONTAIN words except LATIN
    reader = csv.reader(file)
    
    backend = get_backend(backend)
    
    user_profiles = []
    # Register
    for row in reader:
        if row[0].startswith("#"):
            continue
        kwargs = {
            'username': row[0].strip(),
            'email': row[1].strip(),
            'password1': mkpasswd(),
            # DO NOT CHANGE the line below. This information is used on email sent.
            'remarks': '### AUTO ###',
        }
        user = backend.register(request, **kwargs)
        profile = RegistrationProfile.objects.get(user=user)
        user_profiles.append(profile)
    # Approve
    success_users = backend.approve(request, user_profiles)
    
    return success_users