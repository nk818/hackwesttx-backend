#!/usr/bin/env python3
"""
Test database setup locally
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    print("🧪 Testing database setup locally...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # Check if tables exist
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]
            print(f"📊 Found {len(tables)} tables: {tables}")
            
            # Check for api_user table specifically
            if 'api_user' in tables:
                print("✅ api_user table exists")
            else:
                print("❌ api_user table missing")
                
            # Check for auth_user table
            if 'auth_user' in tables:
                print("✅ auth_user table exists")
            else:
                print("❌ auth_user table missing")
        
        # Check superuser
        from django.contrib.auth import get_user_model
        User = get_user_model()
        superusers = User.objects.filter(is_superuser=True)
        print(f"👤 Found {superusers.count()} superuser(s)")
        
        for user in superusers:
            print(f"   - {user.username} ({user.email})")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
