#!/usr/bin/env python
"""
Ensure database is properly set up with all tables
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection

def ensure_database():
    """Ensure database is properly set up"""
    print("🔍 Checking database setup...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # Check if api_user table exists
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_user';")
        result = cursor.fetchone()
        
        if not result:
            print("❌ api_user table missing, creating migrations...")
            # Create migrations
            execute_from_command_line(['manage.py', 'makemigrations', 'api', '--verbosity=2'])
            execute_from_command_line(['manage.py', 'makemigrations', '--verbosity=2'])
            
            # Apply migrations
            print("📊 Applying migrations...")
            execute_from_command_line(['manage.py', 'migrate', '--verbosity=2', '--run-syncdb'])
            
            # Verify table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_user';")
            result = cursor.fetchone()
            if result:
                print("✅ api_user table created successfully")
            else:
                print("❌ Failed to create api_user table")
                return False
        else:
            print("✅ api_user table exists")
        
        # Create superuser if it doesn't exist
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@hackwesttx.com', 'admin123')
            print('✅ Superuser created: admin/admin123')
        else:
            print('✅ Superuser already exists')
        
        print("✅ Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

if __name__ == '__main__':
    success = ensure_database()
    if not success:
        sys.exit(1)
