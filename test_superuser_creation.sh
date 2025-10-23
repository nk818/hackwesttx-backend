#!/bin/bash

echo "🧪 Testing superuser creation with environment variables..."

# Set environment variables (as per Django documentation)
export DJANGO_SUPERUSER_USERNAME="testadmin"
export DJANGO_SUPERUSER_EMAIL="test@hackwesttx.com"
export DJANGO_SUPERUSER_PASSWORD="testpass123"

# Set Django settings
export DJANGO_SETTINGS_MODULE=hackwesttx.settings

# Ensure database exists
touch db.sqlite3
chmod 664 db.sqlite3

# Run migrations
echo "📊 Running migrations..."
python3 manage.py migrate --verbosity=2

# Test superuser creation
echo "👤 Testing superuser creation..."
python3 manage.py createsuperuser --no-input

echo "✅ Test completed! Check if superuser was created."
echo "   Username: $DJANGO_SUPERUSER_USERNAME"
echo "   Email: $DJANGO_SUPERUSER_EMAIL"
