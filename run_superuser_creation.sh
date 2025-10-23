#!/bin/bash

echo "👤 Running superuser creation script..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=hackwesttx.settings

# Ensure database file exists
touch db.sqlite3
chmod 664 db.sqlite3

# Run migrations first
echo "📊 Running migrations..."
python3 manage.py migrate --verbosity=2

# Create superuser
echo "👤 Creating superuser..."
python3 create_superuser_simple.py

echo "✅ Superuser creation process completed!"
