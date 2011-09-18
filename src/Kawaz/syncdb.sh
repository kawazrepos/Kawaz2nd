#!/bin/sh
#
# Install debug fixtures
#
# Author:	alisue
# Date:		2010/12/10
#
cd `dirname $0`
ROOT=`pwd`
DATABASE="/../../kawaz.db"

export DJANGO_SETTINGS_MODULE=Kawaz.settings

while true
do
	echo "Do you want to install fixtures for debug?: [y/n]"
	echo "!!! WARNING !!! Installing fixtures for debug will DESTROY database. !!! WARNING !!!"
	read ans
	case ${ans} in
	[Yy]|[Yy][Ee][Ss])
		rm $ROOT/$DATABASE
		yes no |python $ROOT/manage.py syncdb
		python $ROOT/manage.py loaddata "profiles/fixtures/debug"
		python $ROOT/manage.py loaddata "projects/fixtures/debug"
		python $ROOT/manage.py loaddata debug
		echo "Remodifing object permission... This may take a minute."
		python $ROOT/manage.py remodify_object_permission
		echo "Resave objects... This may take a minute."
		python $ROOT/manage.py resave
		exit 0;;
	[Nn]|[Nn][Oo])
		yes no | python $ROOT/manage.py syncdb
		echo "Remodifing object permission... This may take a minute."
		python $ROOT/manage.py remodify_object_permission
		exit 0;;
	*) 
		echo "Please input 'yes' or 'no'."
		continue;;
	esac
done
