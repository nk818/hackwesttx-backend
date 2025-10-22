#!/usr/bin/env python3
"""
Run Django migrations and create superuser
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    print("🔧 Running Django setup...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # Run migrations
        print("📊 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        print("✅ Migrations completed")
        
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
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
