#!/bin/bash

# Railway startup script for Django
echo "🚀 Starting HackWestTX Backend on Railway..."

# Set environment variables if not set
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-hackwesttx.settings}
export DEBUG=${DEBUG:-False}
export ALLOWED_HOSTS=${ALLOWED_HOSTS:-"*"}

echo "📋 Environment Variables:"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "DEBUG: $DEBUG"
echo "ALLOWED_HOSTS: $ALLOWED_HOSTS"

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# Collect static files (if needed)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start Django server
echo "🌐 Starting Django server on port $PORT..."
python manage.py runserver 0.0.0.0:$PORT
