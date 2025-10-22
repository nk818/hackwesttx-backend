#!/bin/bash

echo "🚀 Starting HackWestTX Backend on Render..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=hackwesttx.settings

# Run database migrations and create superuser
echo "📊 Running database setup..."
python run_migrations.py

# Start the server with gunicorn
echo "🌐 Starting Gunicorn server..."
exec gunicorn hackwesttx.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
