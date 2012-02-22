#!/bin/bash
#
# A Patch for fixing piston issue 205
#
# ref: https://bitbucket.org/jespern/django-piston/issue/205/test-cases-failure-because-fixtures-are
#
PISTON=`python -c "import piston; print piston.__path__[0]"`
cd $PISTON
mkdir fixtures
cd fixtures
wget https://bitbucket.org/jespern/django-piston/raw/4fe8af1db59d/piston/fixtures/models.json

