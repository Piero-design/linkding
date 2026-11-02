"""Ajustes del despliegue académico gratuito de Linkding en Render.

Solo configura el alojamiento; no cambia las funciones del producto.
"""
import os
from urllib.parse import parse_qs, unquote, urlparse


def database_config(connection_url):
    parsed = urlparse(connection_url)
    if parsed.scheme not in {'postgres', 'postgresql'}:
        raise RuntimeError('DATABASE_URL debe ser una conexión PostgreSQL.')
    if not all([parsed.hostname, parsed.username, parsed.password, parsed.path.strip('/')]):
        raise RuntimeError('DATABASE_URL está incompleta. Revisar su valor en Render.')
    options = parse_qs(parsed.query)
    sslmode = options.get('sslmode', ['require'])[0]
    if sslmode not in {'require', 'verify-ca', 'verify-full'}:
        raise RuntimeError('La conexión PostgreSQL debe exigir TLS.')
    connection_options = {'sslmode': sslmode, 'connect_timeout': 15, 'prepare_threshold': None}
    if 'channel_binding' in options:
        connection_options['channel_binding'] = options['channel_binding'][0]
    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': unquote(parsed.path.lstrip('/')),
        'USER': unquote(parsed.username),
        'PASSWORD': unquote(parsed.password),
        'HOST': parsed.hostname,
        'PORT': parsed.port or 5432,
        'OPTIONS': connection_options,
        'CONN_MAX_AGE': 0,
        'DISABLE_SERVER_SIDE_CURSORS': True,
    }


SECRET_KEY = os.environ.get('LINKDING_SECRET_KEY', '')
if len(SECRET_KEY) < 32:
    raise RuntimeError('Falta LINKDING_SECRET_KEY estable. Render puede generarla automáticamente.')

DATABASES = {'default': database_config(os.environ.get('DATABASE_URL', ''))}
USE_SQLITE = False
USE_SQLITE_ICU_EXTENSION = False
LD_DB_ENGINE = 'postgres'

host = os.environ.get('RENDER_EXTERNAL_HOSTNAME', '').strip()
if not host or '/' in host or ':' in host:
    raise RuntimeError('Falta el nombre público de Render en RENDER_EXTERNAL_HOSTNAME.')
ALLOWED_HOSTS = [host, 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://' + host]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
DEBUG = False

# El plan gratuito no conserva archivos locales tras reinicios.
# Las cuentas, los marcadores, las notas y las etiquetas permanecen en PostgreSQL mientras la base esté vigente.
LD_DISABLE_BACKGROUND_TASKS = True
LD_ENABLE_REFRESH_FAVICONS = False
LD_ENABLE_SNAPSHOTS = False
LD_DISABLE_ASSET_UPLOAD = True
TIME_ZONE = 'America/Lima'
