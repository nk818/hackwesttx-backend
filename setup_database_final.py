#!/usr/bin/env python
"""
Final database setup script for Render deployment
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection

def setup_database():
    """Setup database with comprehensive migration handling"""
    print("🔍 Setting up database...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # Apply all migrations systematically
        print("📊 Applying contenttypes migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'contenttypes', '--verbosity=2'])
        
        print("📊 Applying auth migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'auth', '--verbosity=2'])
        
        print("📊 Applying admin migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'admin', '--verbosity=2'])
        
        print("📊 Applying sessions migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'sessions', '--verbosity=2'])
        
        print("📊 Applying authtoken migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'authtoken', '--verbosity=2'])
        
        print("📊 Applying api migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'api', '--verbosity=2'])
        
        # Verify auth_user table exists
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
        result = cursor.fetchone()
        
        if not result:
            print("❌ auth_user table still missing, trying run-syncdb...")
            execute_from_command_line(['manage.py', 'migrate', '--run-syncdb', '--verbosity=2'])
            
            # Check again
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
            result = cursor.fetchone()
            if not result:
                print("❌ Failed to create auth_user table")
                return False
        
        print("✅ auth_user table exists")
        
        # Create superuser
        print("👤 Creating superuser...")
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
    success = setup_database()
    if not success:
        sys.exit(1)
