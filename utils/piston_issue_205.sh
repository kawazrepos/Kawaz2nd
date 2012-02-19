#!/bin/bash
#
# A Patch for fixing piston issue 205
#
# ref: https://bitbucket.org/jespern/django-piston/issue/205/test-cases-failure-because-fixtures-are
#
SITE_PACKAGES=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
cd $SITE_PACKAGES/piston
mkdir fixtures
cd fixtures
wget https://bitbucket.org/jespern/django-piston/raw/4fe8af1db59d/piston/fixtures/models.json

