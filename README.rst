************
 README
************

Kawaz Buillboard Branch

How to install
==========================
::
    
    cd /var/www
    git clone git://github.com/kawazrepos/Kawaz.git Kawaz.buillboard
    git checkout origin/buillboard
    sudo ln -sf /var/www/Kawaz.buillboard/conf/buillboard.kawaz.org /etc/apache2/sites-available/
    
How to use
====================
::

    sudo a2dissite www.kawaz.org
    sudo a2ensite buillboard.kawaz.org
    sudo service apache2 reload
