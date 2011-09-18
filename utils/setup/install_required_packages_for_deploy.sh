#!/bin/sh
PLATFORM=`uname`
echo "***************************************************"
echo
echo "Install required packages for deploy"
echo 
echo "***************************************************"
echo

if [ "$PLATFORM" = "Darwin" ]; then
    echo "Sorry, your platform is not supported yet."
    exit 1
fi

echo "This script will install packages below::"
echo "  - Apache2 + mod_wsgi"
echo "  - MySQL Server"
echo "  - memcached"
echo "  - CSSTidy"
echo "  - python-mysqldb"
echo "  - python-imaging"
echo "  - python-profiler"
echo "  - python-svn"
echo
echo "Do you really want to install these packages for deploy? (y/N)"
read INPUT

if [ "$INPUT" = "y" ]; then
	yes | apt-get install python-setuptools python-pip
	yes | apt-get install python-mysqldb python-imaging python-profiler python-svn
	yes | apt-get install csstidy
	yes | apt-get install apache2 libapache2-mod-wsgi
	yes | apt-get install mysql-server
	yes | apt-get install memcached
fi
