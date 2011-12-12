#!/usr/bin/env python
# vim: set fileencoding=utf8:
from setuptools import setup, find_packages

version = '0.314159'

def read(filename):
    import os.path
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename).read()

setup(
    name="Kawaz",
    version=version,
    description = "Social Network Service for Game Creator live in Sapporo",
    long_description=read('README.rst'),
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords = "django kawaz SNS",
    author = "Alisue",
    author_email = "lambdalisue@hashnote.net",
    url=r"https://github.com/kawazrepos/Kawaz.git",
    download_url = r"https://github.com/kawazrepos/Kawaz/tarball/master",
    packages = find_packages(exclude=['ez_setup']),
    include_package_data = True,
    zip_safe = False,
    test_suite='nose.collector',
    tests_require=['Nose'],
    install_requires=[
        'setuptools',
        'setuptools-git',
        'nose',
        'dateutils',
        'docutils',
        'pyyaml',
        'PIL',
        'django>=1.3',
        'django-nose',
        'django-filter',
        'django-qwert',
        'django-object-permission',
        'django-universaltag',
        'django-googlemap-widget',
    ],
    dependency_links = [
        'https://github.com/alex/django-filter/zipball/master#egg=django-filter',
    ],
)
