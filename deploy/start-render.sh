#!/bin/sh
set -eu

cd /etc/linkding
mkdir -p data/assets data/favicons data/previews

# Migrar al arrancar: la base persiste en Neon, fuera del disco efímero de Render.
python manage.py migrate --no-input
python manage.py create_initial_superuser
chown -R www-data:www-data data

exec uwsgi --http "0.0.0.0:${PORT:-10000}" uwsgi.ini
