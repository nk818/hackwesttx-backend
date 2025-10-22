#!/bin/bash

echo "🚀 Starting HackWestTX Backend (Simple Server with Auto-Migrations)..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=hackwesttx.settings

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Ensure database file exists and is writable
touch db.sqlite3
chmod 664 db.sqlite3

# Run auto-migration script
echo "🔧 Running auto-migration script..."
python3 auto_migrate.py

# Collect static files
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput --verbosity=2

# Start the server
echo "🌐 Starting Gunicorn server..."
exec gunicorn hackwesttx.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
