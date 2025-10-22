#!/usr/bin/env python3
"""
Manual migration script for Render deployment
Run this to ensure all migrations are applied
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    print("🔧 Running manual migrations...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # Check current migration status
        print("📊 Checking migration status...")
        execute_from_command_line(['manage.py', 'showmigrations'])
        
        # Run makemigrations
        print("📝 Creating migrations...")
        execute_from_command_line(['manage.py', 'makemigrations', '--verbosity=2'])
        
        # Run migrations
        print("🚀 Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb', '--verbosity=2'])
        
        # Check final status
        print("✅ Final migration status:")
        execute_from_command_line(['manage.py', 'showmigrations'])
        
        # Create superuser
        print("👤 Creating superuser...")
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@hackwesttx.com',
                password='admin123'
            )
            print("✅ Superuser created: admin/admin123")
        else:
            print("✅ Superuser already exists")
        
        # Collect static files
        print("📁 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--verbosity=2'])
        
        print("🎉 Manual migrations completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
