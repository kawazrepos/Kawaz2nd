#!/bin/sh
cd `dirname $0`
ROOT=`pwd`

NAME="Kawaz"
USER="www-data"
GROUP="www-data"
DIRECTORY="$ROOT/../../"

echo "Changing owner to $USER:$GROUP"
chown -R $USER:$GROUP $DIRECTORY

echo "Changing directory permission to 755"
find $DIRECTORY -type d -exec chmod 755 {} \;

echo "Changing file permission to 644"
find $DIRECTORY -type f -exec chmod 644 {} \;

echo "Changing shell permission to 744"
find $DIRECTORY -type f -name "*.sh" -exec chmod 744 {} \;

echo "Changing permissions of local_settings.py and local_site.py to 640"
chmod 640 $DIRECTORY/src/$NAME/local_settings.py
chmod 640 $DIRECTORY/src/$NAME/local_settings.pyc
chmod 640 $DIRECTORY/src/$NAME/local_site.py
chmod 640 $DIRECTORY/src/$NAME/local_site.pyc
echo "Done. You have to confirm that you can access to the website correctly."
