#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Unittest module of models.Service


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
from nose.tools import *
from test_models_profile import _create_user
from test_models_profile import _delete_user

foo = None
profile = None
service = None

def setup():
    global foo, profile, service
    # create user, profile
    foo, profile = _create_user()

def teardown():
    # delete user, profile
    _delete_user(foo)
