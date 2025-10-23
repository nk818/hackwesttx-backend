#!/usr/bin/env python3
"""
Start fresh with clean migrations
"""

import os
import sys
import django
from django.core.management import call_command
from django.db import connection

def start_fresh():
    """Start fresh with clean migrations"""
    print("🔄 Starting Fresh Migration Process...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # Remove all migration files
        print("🗑️  Removing all migration files...")
        import shutil
        if os.path.exists('api/migrations'):
            shutil.rmtree('api/migrations')
            os.makedirs('api/migrations')
            with open('api/migrations/__init__.py', 'w') as f:
                f.write('')
            print("✅ Removed all api migrations")
        
        # Create fresh initial migration
        print("📊 Creating fresh initial migration...")
        call_command('makemigrations', 'api', verbosity=2)
        
        # Apply migrations
        print("📊 Applying fresh migrations...")
        call_command('migrate', 'api', '--run-syncdb', verbosity=2)
        
        # Verify table exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_user';")
            if not cursor.fetchone():
                print("❌ api_user table does not exist, trying to create it...")
                call_command('migrate', 'api', '--fake-initial', verbosity=2)
        
        # Create superuser
        from api.models import User
        try:
            if not User.objects.filter(is_superuser=True).exists():
                print("👤 Creating superuser...")
                User.objects.create_superuser(
                    username='admin',
                    email='admin@hackwesttx.com',
                    password='admin123'
                )
                print("✅ Superuser created: admin/admin123")
            else:
                print("✅ Superuser already exists")
        except Exception as e:
            print(f"⚠️  Could not create superuser: {e}")
            print("   This is okay, superuser can be created later")
        
        print("✅ Fresh start completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to start fresh: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = start_fresh()
    if not success:
        sys.exit(1)
