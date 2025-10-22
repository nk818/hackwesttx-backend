#!/usr/bin/env python
"""
Fixed database setup script for Render deployment
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

def setup_database():
    """Setup database with proper error handling"""
    print("🚀 Setting up database...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # Create migrations
        print("📊 Creating migrations...")
        execute_from_command_line(['manage.py', 'makemigrations', 'api', '--verbosity=2'])
        execute_from_command_line(['manage.py', 'makemigrations', '--verbosity=2'])
        
        # Apply migrations
        print("📊 Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb', '--verbosity=2', '--fake-initial'])
        
        # Create superuser
        print("👤 Creating superuser...")
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@hackwesttx.com', 'admin123')
            print('✅ Superuser created: admin/admin123')
        else:
            print('✅ Superuser already exists')
        
        # Collect static files
        print("📁 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--verbosity=2'])
        
        print("✅ Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

if __name__ == '__main__':
    success = setup_database()
    if not success:
        sys.exit(1)
