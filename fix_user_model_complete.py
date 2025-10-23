#!/usr/bin/env python3
"""
Complete fix for user model - handles the transition from default User to custom User
"""

import os
import sys
import django
from django.core.management import call_command
from django.db import connection

def fix_user_model_complete():
    """Complete fix for user model"""
    print("🔧 Complete User Model Fix...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # First, let's check what tables exist
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"📊 Existing tables: {tables}")
        
        # Delete the problematic migration
        print("🗑️  Removing problematic migration...")
        migration_file = 'api/migrations/0002_user.py'
        if os.path.exists(migration_file):
            os.remove(migration_file)
            print("✅ Removed 0002_user.py")
        
        # Reset migrations for api app
        print("🔄 Resetting api migrations...")
        call_command('migrate', 'api', 'zero', verbosity=2)
        
        # Create fresh migrations
        print("📊 Creating fresh migrations...")
        call_command('makemigrations', 'api', verbosity=2)
        
        # Apply migrations
        print("📊 Applying fresh migrations...")
        call_command('migrate', 'api', verbosity=2)
        
        # Create superuser
        from api.models import User
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
        
        # Verify the user table exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_user';")
            if cursor.fetchone():
                print("✅ Custom User table (api_user) exists")
            else:
                print("❌ Custom User table (api_user) does not exist")
                return False
        
        print("✅ Complete user model fix completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to fix user model: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = fix_user_model_complete()
    if not success:
        sys.exit(1)
