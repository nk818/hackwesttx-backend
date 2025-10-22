#!/bin/bash

echo "🚀 Starting HackWestTX Backend (Simple Version)..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=hackwesttx.settings

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Ensure database file exists
touch db.sqlite3

# Run database migrations
echo "📊 Running database migrations..."
python manage.py makemigrations --verbosity=2
python manage.py migrate --run-syncdb --verbosity=2

# Create superuser
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@hackwesttx.com', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('✅ Superuser already exists')
"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --verbosity=2

# Start the server
echo "🌐 Starting Gunicorn server..."
exec gunicorn hackwesttx.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
