#!/bin/bash

# Render startup script for Django backend
echo "🚀 Starting HackWestTX Backend on Render..."

# Run database migrations
echo "📊 Running database migrations..."
python manage.py migrate

# Start the server with gunicorn
echo "🌐 Starting Gunicorn server..."
exec gunicorn hackwesttx.wsgi:application --bind 0.0.0.0:$PORT
