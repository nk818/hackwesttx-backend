#!/bin/bash
# Railway startup script to ensure migrations run properly

echo "🚀 Starting Railway deployment..."

# Check if database exists
if [ ! -f "/tmp/db.sqlite3" ]; then
    echo "📊 Creating new database..."
    touch /tmp/db.sqlite3
fi

# Run migrations
echo "🔄 Running database migrations..."
python manage.py migrate --run-syncdb

# Check if migrations were successful
if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully!"
else
    echo "❌ Migrations failed!"
    exit 1
fi

# Start the Django server
echo "🌐 Starting Django server..."
python manage.py runserver 0.0.0.0:$PORT
