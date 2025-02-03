# # #!/bin/sh

# # echo "Going to run migrations"
# # virtualenv run python manage.py migrate

# # echo "Going to run django server"
# # virtualenv run python manage.py runserver 0.0.0.0:8000

# #!/bin/bash

# # Exit the script immediately if a command fails
# set -e

# # Apply database migrations
# echo "Applying database migrations..."
# python manage.py migrate --noinput

# # Collect static files
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# # Start the Gunicorn server
# echo "Starting the Gunicorn server..."
# exec gunicorn django-ledger.wsgi:application --bind 0.0.0.0:8000 --workers=3




#!/bin/sh

# Exit on error
set -e

# Apply database migrations
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Start Gunicorn server
exec gunicorn --workers 3 --bind 0.0.0.0:8000 django-ledger.wsgi:application
