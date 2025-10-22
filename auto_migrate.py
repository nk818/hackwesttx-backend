#!/usr/bin/env python3
"""
Auto-migration script for Render free tier
This script runs migrations and creates superuser automatically
"""

import os
import sys
import django
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import connection

def run_migrations():
    """Run Django migrations"""
    print("📊 Running Django migrations...")
    try:
        call_command('migrate', verbosity=2)
        print("✅ Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def create_superuser():
    """Create superuser if it doesn't exist"""
    print("👤 Checking for superuser...")
    try:
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@hackwesttx.com', 'admin123')
            print("✅ Superuser 'admin' created successfully!")
        else:
            print("✅ Superuser already exists!")
        return True
    except Exception as e:
        print(f"❌ Superuser creation failed: {e}")
        return False

def verify_database():
    """Verify database tables exist"""
    print("🔍 Verifying database tables...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]
            print(f"✅ Database tables: {table_names}")
            
            # Check for critical tables
            critical_tables = ['auth_user', 'django_migrations', 'django_content_type']
            missing_tables = [table for table in critical_tables if table not in table_names]
            
            if missing_tables:
                print(f"⚠️  Missing critical tables: {missing_tables}")
                return False
            else:
                print("✅ All critical tables exist!")
                return True
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False

def main():
    """Main function to run all setup tasks"""
    print("🚀 Starting Auto-Migration Script...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    # Run migrations
    if not run_migrations():
        print("❌ Migration failed, exiting...")
        sys.exit(1)
    
    # Create superuser
    if not create_superuser():
        print("❌ Superuser creation failed, exiting...")
        sys.exit(1)
    
    # Verify database
    if not verify_database():
        print("❌ Database verification failed, exiting...")
        sys.exit(1)
    
    print("🎉 Auto-migration completed successfully!")
    return True

if __name__ == '__main__':
    main()
