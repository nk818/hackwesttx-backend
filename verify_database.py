#!/usr/bin/env python3
"""
Verify database setup on Render
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    print("🔍 Verifying database setup...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # Check database tables
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]
            print(f"📊 Found {len(tables)} tables")
            
            # Check for important tables
            important_tables = ['api_user', 'auth_user', 'django_admin_log', 'django_migrations']
            for table in important_tables:
                if table in tables:
                    print(f"   ✅ {table} exists")
                else:
                    print(f"   ❌ {table} missing")
            
            # Check api_user table specifically
            if 'api_user' in tables:
                cursor.execute("SELECT COUNT(*) FROM api_user")
                count = cursor.fetchone()[0]
                print(f"   📊 api_user has {count} records")
            else:
                print("   ❌ api_user table missing - this is the problem!")
                
        # Check superuser
        from django.contrib.auth import get_user_model
        User = get_user_model()
        superusers = User.objects.filter(is_superuser=True)
        print(f"👤 Found {superusers.count()} superuser(s)")
        
        if superusers.count() == 0:
            print("   ❌ No superusers found - creating one...")
            User.objects.create_superuser('admin', 'admin@hackwesttx.com', 'admin123')
            print("   ✅ Superuser created")
        
        print("🎉 Database verification completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
