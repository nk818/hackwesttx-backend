#!/usr/bin/env python3
"""
Render CLI Migration Script
Run this as a one-time job on Render
"""

import os
import sys
import django
from django.core.management import call_command
from django.contrib.auth import get_user_model

def main():
    print("🚀 Starting Render CLI Migration Script...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    print("📊 Running Django migrations...")
    try:
        # Run all migrations
        call_command('migrate', verbosity=2)
        print("✅ Migrations completed successfully!")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)
    
    print("👤 Creating superuser...")
    try:
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@hackwesttx.com', 'admin123')
            print("✅ Superuser 'admin' created successfully!")
        else:
            print("✅ Superuser already exists!")
    except Exception as e:
        print(f"❌ Superuser creation failed: {e}")
        sys.exit(1)
    
    print("🔍 Verifying database tables...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"✅ Database tables: {[table[0] for table in tables]}")
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        sys.exit(1)
    
    print("🎉 All migrations and setup completed successfully!")

if __name__ == '__main__':
    main()
