#!/bin/sh

echo "Going to run migrations"
virtualenv run python manage.py migrate

echo "Going to run django server"
virtualenv run python manage.py runserver 0.0.0.0:8000