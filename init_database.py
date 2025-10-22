#!/usr/bin/env python3
"""
Initialize database on Render deployment
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    print("🔧 Initializing database on Render...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # Check if database file exists
        from django.conf import settings
        db_path = settings.DATABASES['default']['NAME']
        print(f"📊 Database path: {db_path}")
        
        if os.path.exists(db_path):
            print(f"✅ Database file exists: {db_path}")
            file_size = os.path.getsize(db_path)
            print(f"   File size: {file_size} bytes")
        else:
            print(f"⚠️  Database file missing: {db_path}")
            print("   Creating database file...")
            # Create the database file
            with open(db_path, 'w') as f:
                pass
            print("   ✅ Database file created")
        
        # Run migrations
        print("📊 Running migrations...")
        execute_from_command_line(['manage.py', 'makemigrations', '--verbosity=2'])
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb', '--verbosity=2'])
        
        # Verify api_user table
        print("🔍 Verifying api_user table...")
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_user';")
            result = cursor.fetchone()
            if result:
                print("✅ api_user table exists")
                
                # Check table structure
                cursor.execute("PRAGMA table_info(api_user)")
                columns = cursor.fetchall()
                print(f"   Table has {len(columns)} columns")
                
                # Check if table has data
                cursor.execute("SELECT COUNT(*) FROM api_user")
                count = cursor.fetchone()[0]
                print(f"   Records: {count}")
            else:
                print("❌ api_user table missing")
                return False
        
        # Create superuser
        print("👤 Creating superuser...")
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@hackwesttx.com', 'admin123')
            print("✅ Superuser created: admin/admin123")
        else:
            print("✅ Superuser already exists")
        
        print("🎉 Database initialization completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
