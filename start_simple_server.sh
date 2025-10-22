#!/bin/bash

echo "🚀 Starting HackWestTX Backend (Simple Server)..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=hackwesttx.settings

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Ensure database file exists
touch db.sqlite3

# Collect static files
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput --verbosity=2

# Start the server
echo "🌐 Starting Gunicorn server..."
exec gunicorn hackwesttx.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
