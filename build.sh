#!/bin/bash

echo "🔨 Starting build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt || pip install -r requirements_minimal.txt

# Create staticfiles directory
mkdir -p staticfiles

# Ensure database file exists
touch db.sqlite3
chmod 664 db.sqlite3

# Run migrations
echo "📊 Running Django migrations..."
python3 manage.py migrate --verbosity=2

# Create superuser if environment variable is set
if [[ $CREATE_SUPERUSER ]]; then
    echo "👤 Creating superuser (triggered by CREATE_SUPERUSER env var)..."
    python3 manage.py createsuperuser --no-input \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
    echo "✅ Superuser created: $DJANGO_SUPERUSER_USERNAME"
else
    echo "⏭️  Skipping superuser creation (CREATE_SUPERUSER not set)"
fi

# Collect static files
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput --verbosity=2

echo "🎉 Build completed successfully!"
