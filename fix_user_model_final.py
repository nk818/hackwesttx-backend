#!/usr/bin/env python3
"""
Fix user model and create proper migrations
"""

import os
import sys
import django
from django.core.management import call_command
from django.db import connection

def fix_user_model():
    """Fix the user model by creating proper migrations"""
    print("🔧 Fixing User Model...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # Create migrations for the api app
        print("📊 Creating migrations for api app...")
        call_command('makemigrations', 'api', verbosity=2)
        
        # Apply migrations
        print("📊 Applying migrations...")
        call_command('migrate', 'api', verbosity=2)
        
        # Check if we need to create a superuser
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
        
        print("✅ User model fix completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to fix user model: {e}")
        return False

if __name__ == '__main__':
    success = fix_user_model()
    if not success:
        sys.exit(1)
