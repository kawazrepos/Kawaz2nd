#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
short module explanation

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
__VERSION__ = "0.31415rc3"
from setuptools import setup, find_packages

def read(filename):
    import os.path
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename).read()
def is_deploy():
    import imp
    import os.path
    path = os.path.join(os.path.dirname(__file__), 'src/Kawaz')
    try:
        args = imp.find_module('local_settings', [path])
        module = imp.load_module('local_settings', *args)
        return module.DEBUG == False
    except ImportError:
        return False

INSTALL_REQUIRES = [
    'distribute',
    'setuptools',
    'setuptools-git',
    'dateutils',
    'docutils',
    'pyyaml',
    'markdown',
    'BeautifulSoup',
    'gdata',
    'whoosh==1.1.1',
    'south',
    'PIL',  
    'django==1.2.3',
    'django-compress',
    'django-reversetag',
    'django-pagination',
    'django-haystack==1.1',
    'django-markupfield',
]
if is_deploy():
    print("*"*80)
    print(" Install requirements on Deploy mode.")
    print("")
    print(" Note: Install requirements package as Deploy mode because")
    print("       You have set the following lines on 'local_settings.py'")
    print("")
    print("       DEBUG=False")
    print("")
    print("*"*80)
    INSTALL_REQUIRES += [
        'pysolr',
        'MySQL-python',
        'python-memcached',
    ]
else:
    print("*"*80)
    print(" Install requirements on Develop mode.")
    print("")
    print(" Note: If you want to install requirements package as Deploy mode.")
    print("       Add the following lines on 'local_settings.py'")
    print("")
    print("       DEBUG=False")
    print("")
    print("*"*80)

setup(
    name="Kawaz",
    version=__VERSION__,
    description = "Social Network Service for Game Creators live in Sapporo",
    long_description=read('README.rst'),
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords = "django creative commons game creator sns",
    author = "Alisue",
    author_email = "lambdalisue@hashnote.net",
    url=r"https://github.com/kawazrepos/Kawaz.git",
    download_url = r"https://github.com/kawazrepos/Kawaz/tarball/master",
    packages = find_packages(exclude=['ez_setup']),
    include_package_data = True,
    zip_safe = False,
    test_suite='nose.collector',
    tests_require=['Nose'],
    install_requires=INSTALL_REQUIRES,
    dependency_links=[
        # Use falked version of django-markupfield till my pull request is
        # accepted.
        'https://github.com/lambdalisue/django-markupfield/tarball/master#egg=django_markupfield',
    ],
)
