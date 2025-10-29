#!/usr/bin/env python3
"""
Start fresh with clean migrations
"""

import os
import sys
import django
from django.core.management import call_command
from django.db import connection
from django.conf import settings

def start_fresh():
    """Start fresh with clean migrations"""
    print("🔄 Starting Fresh Migration Process...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # Remove all migration files
        print("🗑️  Removing all migration files...")
        import shutil
        if os.path.exists('api/migrations'):
            shutil.rmtree('api/migrations')
            os.makedirs('api/migrations')
            with open('api/migrations/__init__.py', 'w') as f:
                f.write('')
            print("✅ Removed all api migrations")
        
        # Create fresh initial migration
        print("📊 Creating fresh initial migration...")
        call_command('makemigrations', 'api', verbosity=2)
        
        # Apply migrations for all apps
        print("📊 Applying fresh migrations...")
        call_command('migrate', '--run-syncdb', verbosity=2)
        
        # Force apply api migrations specifically
        print("📊 Force applying api migrations...")
        call_command('migrate', 'api', verbosity=2)
        
        # Verify tables exist
        print("🔍 Verifying database tables...")
        with connection.cursor() as cursor:
            # Detect database engine and use appropriate query
            db_engine = settings.DATABASES['default']['ENGINE']
            
            if 'postgresql' in db_engine:
                # PostgreSQL query
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
                """)
                tables = cursor.fetchall()
                table_names = [table[0] for table in tables]
                
                # Check for api_user table
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = 'api_user';
                """)
                api_user_check = cursor.fetchone()
            else:
                # SQLite query
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                table_names = [table[0] for table in tables]
                
                # Check for api_user table
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_user';")
                api_user_check = cursor.fetchone()
            
            print(f"📊 Found {len(table_names)} tables in database")
            
            if not api_user_check:
                print("❌ api_user table does not exist, trying to create it...")
                call_command('migrate', 'api', '--fake-initial', verbosity=2)
            else:
                print("✅ api_user table exists")
        
        # Create superuser using environment variables
        from api.models import User
        try:
            if not User.objects.filter(is_superuser=True).exists():
                print("👤 Creating superuser...")
                
                # Use environment variables if available
                username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
                email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@hackwesttx.com')
                password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
                
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                print(f"✅ Superuser created: {username}/{password}")
            else:
                print("✅ Superuser already exists")
        except Exception as e:
            print(f"⚠️  Could not create superuser: {e}")
            print("   This is okay, superuser can be created later")
        
        print("✅ Fresh start completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to start fresh: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = start_fresh()
    if not success:
        sys.exit(1)
