************
 README
************

Kawaz Inform Branch

How to install
==========================
::
    
    cd /var/www
    git clone -b info git://github.com/kawazrepos/Kawaz.git Kawaz.info
    sudo ln -sf /var/www/Kawaz.info/conf/info.kawaz.org /etc/apache2/sites-available/
    
How to use
====================
::

    sudo a2dissite www.kawaz.org
    sudo a2ensite info.kawaz.org
    sudo service apache2 reload
