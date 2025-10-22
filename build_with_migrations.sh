#!/bin/bash

echo "🔨 Starting build process with conditional migrations..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt || pip install -r requirements_minimal.txt

# Create staticfiles directory
mkdir -p staticfiles

# Ensure database file exists
touch db.sqlite3
chmod 664 db.sqlite3

# Check if we should run migrations
if [[ -n "$RUN_MIGRATIONS" ]]; then
    echo "📊 Running Django migrations (triggered by RUN_MIGRATIONS env var)..."
    python3 manage.py migrate --verbosity=2
    
    if [[ $? -eq 0 ]]; then
        echo "✅ Migrations completed successfully!"
    else
        echo "❌ Migrations failed!"
        exit 1
    fi
else
    echo "⏭️  Skipping migrations (RUN_MIGRATIONS not set)"
fi

# Check if we should create superuser
if [[ -n "$CREATE_SUPERUSER" ]]; then
    echo "👤 Creating superuser (triggered by CREATE_SUPERUSER env var)..."
    python3 manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@hackwesttx.com', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('✅ Superuser already exists')
"
    
    if [[ $? -eq 0 ]]; then
        echo "✅ Superuser setup completed!"
    else
        echo "❌ Superuser creation failed!"
        exit 1
    fi
else
    echo "⏭️  Skipping superuser creation (CREATE_SUPERUSER not set)"
fi

# Collect static files
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput --verbosity=2

echo "🎉 Build completed successfully!"
