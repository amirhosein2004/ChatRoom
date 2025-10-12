#!/bin/bash

# Production entrypoint script for ChatPage Django application
# Optimized for production deployment with proper error handling and logging

set -e

echo "🚀 Starting ChatPage Production Environment..."

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

# Create logs directory if it doesn't exist
mkdir -p /app/logs

# Start Gunicorn with proper configuration
echo "🎯 Starting Gunicorn server..."
exec gunicorn chat.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class gevent \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --preload \
    --access-logfile /app/logs/gunicorn_access.log \
    --error-logfile /app/logs/gunicorn_error.log \
    --log-level info
