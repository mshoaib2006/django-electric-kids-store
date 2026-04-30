#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Clean old collected static files
rm -rf staticfiles

# Confirm main CSS exists before collecting
python manage.py findstatic css/style.css --verbosity 2

# Collect all static files for Render
python manage.py collectstatic --no-input --clear --verbosity 2

# Apply database migrations
python manage.py migrate
