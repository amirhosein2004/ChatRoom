#!/bin/bash

# Staging entrypoint script for ChatPage Django application
# Production-like environment with additional debugging capabilities

set -e

echo "🚀 Starting ChatPage Staging Environment..."

# Wait for database to be ready with timeout
echo "⏳ Waiting for database connection..."
timeout=60
counter=0
while ! nc -z db 5432; do
  sleep 1
  counter=$((counter + 1))
  if [ $counter -eq $timeout ]; then
    echo "❌ Database connection timeout after ${timeout}s"
    exit 1
  fi
done
echo "✅ Database is ready!"

# Wait for Redis to be ready with timeout
echo "⏳ Waiting for Redis connection..."
counter=0
while ! nc -z redis 6379; do
  sleep 1
  counter=$((counter + 1))
  if [ $counter -eq $timeout ]; then
    echo "❌ Redis connection timeout after ${timeout}s"
    exit 1
  fi
done
echo "✅ Redis is ready!"

# Run database migrations
echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create test superuser for staging (if needed)
echo "👤 Creating staging superuser if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='staging_admin').exists():
    User.objects.create_superuser('staging_admin', 'staging@chatpage.com', 'staging123')
    print('Staging superuser created: staging_admin/staging123')
else:
    print('Staging superuser already exists')
"

# Create logs directory if it doesn't exist
mkdir -p /app/logs

# Start Gunicorn with staging configuration (fewer workers, more logging)
echo "🎯 Starting Gunicorn server for staging..."
exec gunicorn chat.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --worker-class gevent \
    --worker-connections 500 \
    --max-requests 500 \
    --max-requests-jitter 50 \
    --timeout 60 \
    --keep-alive 2 \
    --preload \
    --access-logfile /app/logs/gunicorn_access.log \
    --error-logfile /app/logs/gunicorn_error.log \
    --log-level debug \
    --reload
