#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Clean old collected static files before collecting again
# This prevents stale/missing Cloudinary static files from breaking build
rm -rf staticfiles

python manage.py collectstatic --no-input
python manage.py migrate