#!/usr/bin/env python3
"""
Fix custom user model migration on Render
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    print("🔧 Fixing custom user model migration...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # Check current migration status
        print("📊 Checking migration status...")
        execute_from_command_line(['manage.py', 'showmigrations', 'api'])
        
        # Force create migrations for api app
        print("📝 Creating migrations for api app...")
        execute_from_command_line(['manage.py', 'makemigrations', 'api', '--verbosity=2'])
        
        # Run migrations specifically for api app
        print("🚀 Applying api migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'api', '--verbosity=2'])
        
        # Run all migrations
        print("🚀 Applying all migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb', '--verbosity=2'])
        
        # Verify api_user table exists
        print("🔍 Verifying api_user table...")
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_user';")
            result = cursor.fetchone()
            if result:
                print("✅ api_user table exists")
                
                # Check if table has data
                cursor.execute("SELECT COUNT(*) FROM api_user")
                count = cursor.fetchone()[0]
                print(f"   📊 api_user has {count} records")
            else:
                print("❌ api_user table still missing")
                
                # Try to create the table manually
                print("🔧 Attempting manual table creation...")
                from django.core.management import call_command
                call_command('migrate', 'api', '--fake-initial')
                call_command('migrate', 'api')
                
                # Check again
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_user';")
                result = cursor.fetchone()
                if result:
                    print("✅ api_user table created manually")
                else:
                    print("❌ Manual creation failed")
                    return False
        
        # Create superuser if needed
        print("👤 Checking superuser...")
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(is_superuser=True).exists():
            print("Creating superuser...")
            User.objects.create_superuser('admin', 'admin@hackwesttx.com', 'admin123')
            print("✅ Superuser created: admin/admin123")
        else:
            print("✅ Superuser already exists")
        
        print("🎉 Custom user model fix completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
