#!/bin/bash

echo "🚀 Starting HackWestTX Backend (Final Version)..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=hackwesttx.settings

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Ensure database file exists and is writable
touch db.sqlite3
chmod 664 db.sqlite3

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

# Force create migrations
echo "📊 Creating migrations..."
python3 manage.py makemigrations api --verbosity=2 --noinput
python3 manage.py makemigrations --verbosity=2 --noinput

# Apply ALL migrations including Django's built-in ones
echo "📊 Applying ALL migrations..."
python3 manage.py migrate --verbosity=2 --run-syncdb

# Specifically apply auth migrations
echo "📊 Applying auth migrations..."
python3 manage.py migrate auth --verbosity=2

# Apply admin migrations
echo "📊 Applying admin migrations..."
python3 manage.py migrate admin --verbosity=2

# Apply sessions migrations
echo "📊 Applying sessions migrations..."
python3 manage.py migrate sessions --verbosity=2

# Apply contenttypes migrations
echo "📊 Applying contenttypes migrations..."
python3 manage.py migrate contenttypes --verbosity=2

# Apply authtoken migrations
echo "📊 Applying authtoken migrations..."
python3 manage.py migrate authtoken --verbosity=2

# Apply api migrations
echo "📊 Applying api migrations..."
python3 manage.py migrate api --verbosity=2

# Comprehensive database setup
echo "🔍 Comprehensive database setup..."
python3 setup_database_final.py

# Collect static files
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput --verbosity=2

# Start the server
echo "🌐 Starting Gunicorn server..."
exec gunicorn hackwesttx.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
