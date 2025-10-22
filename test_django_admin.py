#!/usr/bin/env python3
"""
Test Django admin functionality locally
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    print("🧪 Testing Django admin functionality...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # Check if admin is properly configured
        from django.contrib import admin
        from django.contrib.admin.sites import site
        print(f"✅ Django admin is configured")
        print(f"   Registered models: {len(admin.site._registry)}")
        
        # Check static files configuration
        from django.conf import settings
        print(f"✅ Static files configuration:")
        print(f"   STATIC_URL: {settings.STATIC_URL}")
        print(f"   STATIC_ROOT: {settings.STATIC_ROOT}")
        print(f"   STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
        
        # Check if static files directory exists
        static_root = settings.STATIC_ROOT
        if os.path.exists(static_root):
            print(f"✅ Static files directory exists: {static_root}")
            static_files = os.listdir(static_root)
            print(f"   Found {len(static_files)} files/directories")
        else:
            print(f"⚠️  Static files directory missing: {static_root}")
        
        # Check database tables
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]
            print(f"✅ Database has {len(tables)} tables")
            
            # Check for important tables
            important_tables = ['auth_user', 'api_user', 'django_admin_log']
            for table in important_tables:
                if table in tables:
                    print(f"   ✅ {table} exists")
                else:
                    print(f"   ❌ {table} missing")
        
        # Check superuser
        from django.contrib.auth import get_user_model
        User = get_user_model()
        superusers = User.objects.filter(is_superuser=True)
        print(f"✅ Found {superusers.count()} superuser(s)")
        
        print("\n🎉 Django admin test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
