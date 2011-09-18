#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:    alisue
# Date:        2010/10/14
#
from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor, sha_constructor

def get_hexdigest(algorithm, salt, raw_password):
    """
    Returns a string of the hexdigest of the given plaintext password and salt
    using the given algorithm ('md5', 'sha1' or 'crypt').
    """
    raw_password, salt = smart_str(raw_password), smart_str(salt)
#    if algorithm == 'crypt':
#        try:
#            import crypt
#        except ImportError:
#            raise ValueError('"crypt" password algorithm not supported in this environment')
#        return crypt.crypt(raw_password, salt)

    if algorithm == 'md5':
        return md5_constructor(salt + raw_password).hexdigest()
    elif algorithm == 'sha1':
        return sha_constructor(salt + raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")

def set_password(raw_password):
    import random
    algo = 'sha1'
    salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(algo, salt, raw_password)
    return '%s$%s$%s' % (algo, salt, hsh)

if __name__ == '__main__':
    import sys
    
    print "Django password generator"
    print "-------------------------------------------------"
    print "Plase input raw password"
    
    raw_password = sys.stdin.readline()
    if raw_password.endswith('\n'):
        raw_password = raw_password[:-1]
    print set_password(raw_password)
