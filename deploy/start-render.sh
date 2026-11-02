#!/bin/sh
set -eu

cd /etc/linkding
mkdir -p data/assets data/favicons data/previews
# uWSGI baja a www-data; libpq no debe buscar certificados dentro de /root.
export PGSSLCERT=/etc/linkding/data/postgresql.crt
export PGSSLKEY=/etc/linkding/data/postgresql.key
export PGSSLROOTCERT=/etc/linkding/data/root.crt
export PGSSLCRL=/etc/linkding/data/root.crl

# Migrar al arrancar: PostgreSQL persiste fuera del disco efímero del servicio.
python manage.py migrate --no-input
python manage.py create_initial_superuser
chown -R www-data:www-data data

# Verificar la conexión con el mismo usuario sin privilegios del servidor web.
python - <<'PYTHON'
import os
import pwd
import django
account = pwd.getpwnam("www-data")
os.setgid(account.pw_gid)
os.setuid(account.pw_uid)
django.setup()
from django.db import connections
connections["default"].ensure_connection()
connections.close_all()
print("PostgreSQL: conexión verificada como www-data con TLS", flush=True)
PYTHON

# Un único socket HTTP evita que el detector de puertos pruebe un socket uWSGI.
exec uwsgi --ini uwsgi.ini --http-socket "0.0.0.0:${PORT:-10000}"
