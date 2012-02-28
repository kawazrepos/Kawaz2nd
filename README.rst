How to install
============================

1.  Run ``python setup.py develop`` to install Kawaz

How to test
======================

Run ``python setup.py test`` for minimu test and

Run ``python src/kawaz/manage.py test`` for full test

How to run
====================

Not yet.


PermissionGroup?
================================

Authenticated users
--------------------------------------

zeele
    User can promote to superuser. These users also belong to ``nerv`` and ``children``

nerv
    User can handle (a little bit) settings of Kawaz in Django Admin page.
    These users also belong to ``children``

children
    User registered in Kawaz with registration page.
    These user can create events, blog, project ...etc

visitor
    User registered in Kawaz with OpenID. 
    These user can post comments and attend events.

Anonymous users
------------------------------

They just can see the public page. No attending events and posting comments.
