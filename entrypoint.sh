#!/bin/bash

echo "Waiting for PostgreSQL..."
for i in $(seq 1 30); do
    if python -c "
import socket, os
host = os.environ.get('POSTGRES_HOST', 'db')
port = int(os.environ.get('POSTGRES_PORT', 5432))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)
s.connect((host, port))
s.close()
" 2>/dev/null; then
        echo "PostgreSQL is up."
        break
    fi
    echo "Attempt $i/30..."
    sleep 1
done

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting application..."
exec "$@"
