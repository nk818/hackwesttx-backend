#!/bin/bash

echo "🚀 Starting HackWestTX Backend on Render..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=hackwesttx.settings

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Ensure database directory exists
touch db.sqlite3

# Function to check if migrations ran successfully
check_migrations() {
    echo "🔍 Checking if migrations were successful..."
    python manage.py shell -c "
import os
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\")
    tables = [table[0] for table in cursor.fetchall()]
    print(f'Found {len(tables)} tables: {tables[:10]}...')
    if 'api_user' in tables:
        print('✅ api_user table exists')
    else:
        print('❌ api_user table missing')
        exit(1)
"
}

# Initialize database properly
echo "🔧 Initializing database..."
python init_database.py || {
    echo "❌ Database initialization failed, trying alternative approach..."
    python manage.py makemigrations --verbosity=2
    python manage.py migrate --run-syncdb --verbosity=2
    python fix_user_model.py
}

# Check if migrations were successful
check_migrations || {
    echo "❌ Migrations still failed, trying manual table creation..."
    python manage.py shell -c "
from django.core.management import execute_from_command_line
import sys
try:
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    print('✅ Manual migration successful')
except Exception as e:
    print(f'❌ Manual migration failed: {e}')
    sys.exit(1)
"
}

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@hackwesttx.com', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('✅ Superuser already exists')
" || echo "⚠️ Superuser creation failed, continuing..."

# Collect static files for Django admin
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --verbosity=2

# Final verification
echo "🔍 Final verification..."
check_migrations

# Start the server with gunicorn
echo "🌐 Starting Gunicorn server..."
exec gunicorn hackwesttx.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
