#!/bin/bash

# Development entrypoint script for ChatPage Django application
# This script handles database migrations, static files, and starts the development server

set -e

echo "🚀 Starting ChatPage Development Environment..."

# Wait for database to be ready
echo "⏳ Waiting for database connection..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "✅ Database is ready!"

# Wait for Redis to be ready
echo "⏳ Waiting for Redis connection..."
while ! nc -z redis 6379; do
  sleep 0.1
done
echo "✅ Redis is ready!"

# Run database migrations
echo "🔄 Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist (for development)
echo "👤 Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@chatpage.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

echo "🎯 Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000
