#!/bin/bash
#
# This shell script is required for cron
#
export DJANGO_SETTINGS_MODULE=Kawaz.settings
python manage.py ${*}
