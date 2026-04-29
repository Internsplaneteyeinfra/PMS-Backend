#!/bin/bash
set -e

echo "Starting PMC Backend..."

# Wait for external PostgreSQL using DATABASE_URL
echo "Waiting for database..."
until python - <<'EOF'
import os, sys
url = os.environ.get('DATABASE_URL', '')
print(f"DATABASE_URL present: {bool(url)}")
if not url:
    print("ERROR: DATABASE_URL not set")
    sys.exit(1)

# Parse manually to avoid any import issues
from urllib.parse import urlparse
r = urlparse(url)
import psycopg2
try:
    conn = psycopg2.connect(
        dbname=r.path.lstrip('/'),
        user=r.username,
        password=r.password,
        host=r.hostname,
        port=r.port or 5432,
        sslmode='require'
    )
    conn.close()
    print("Database ready.")
except Exception as e:
    print(f"DB not ready: {e}")
    sys.exit(1)
EOF
do
    echo "Retrying in 3s..."
    sleep 3
done

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Daphne..."
exec daphne backend.asgi:application \
    --bind 0.0.0.0 \
    --port ${PORT:-8000} \
    --proxy-headers
