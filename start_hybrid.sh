#!/bin/bash

echo "🚀 Starting HackWestTX Backend (Hybrid SQLite + MongoDB Atlas)..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=hackwesttx.settings

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Ensure database file exists
touch db.sqlite3

# Test MongoDB Atlas connection (optional)
echo "🔍 Testing MongoDB Atlas connection..."
python3 -c "
import os
import sys
try:
    from pymongo import MongoClient
    from pymongo.server_api import ServerApi
    uri = os.environ.get('MONGODB_URI', 'mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    client = MongoClient(uri, server_api=ServerApi('1'), tlsAllowInvalidCertificates=True)
    client.admin.command('ping')
    print('✅ MongoDB Atlas connection successful')
    client.close()
except Exception as e:
    print(f'⚠️  MongoDB Atlas connection failed: {e}')
    print('   Continuing with SQLite only...')
" || echo "⚠️  MongoDB connection test failed, continuing..."

# Run database migrations (SQLite)
echo "📊 Running database migrations..."
python3 manage.py makemigrations --verbosity=2
python3 manage.py migrate --verbosity=2

# Create superuser
echo "👤 Creating superuser..."
python3 manage.py shell -c "
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
python3 manage.py collectstatic --noinput --verbosity=2

# Start the server
echo "🌐 Starting Gunicorn server..."
exec gunicorn hackwesttx.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
