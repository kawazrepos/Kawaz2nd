#!/usr/bin/env python
# vim: set fileencoding=utf8:
from setuptools import setup, find_packages

#version = '0.314159'
version = '3.0.0'

def read(filename):
    import os.path
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename).read()

setup(
    name="Kawaz",
    version=version,
    description = "Social Network Service for Game Creators live in Sapporo",
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
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires=[
        'setuptools',
        'setuptools-git',
        'dateutils',
        'docutils',
        'PyYAML',
        'markdown',
        'gdata',
        'PIL',
        'django>=1.4b1',
        'django-piston',
        'httplib2',
        'django-qwert',
        'django-universaltag>=0.1.6',
        'django-object-permission>=0.5.1',
        'django-inspectional-registration>=0.2.10',
        'django-userel',
        'django-thumbnailfield',
        'django-googlemap-widget>=0.1.3',
        'django-markitup-widget',
        'django-markupfield>=1.0.2dev',
    ],
    dependency_links = [
        # until official django-markupfield fix the issue
        'https://github.com/lambdalisue/django-markupfield/zipball/master#egg=django-markupfield-1.0.2dev',
        # until django officially release 1.4
        'http://www.djangoproject.com/download/1.4-beta-1/tarball/#egg=django-1.4-beta-1',
        # until django-piston support Django 1.4
        'https://bitbucket.org/lambdalisue/django-piston/get/a3a86f9799e8.zip#egg=django-piston'
    ],
    test_suite='runtests.runtests',
)
