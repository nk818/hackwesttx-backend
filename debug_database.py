#!/usr/bin/env python3
"""
Debug Database Issues on Railway
This script helps debug database connection and migration issues
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def debug_database():
    """Debug database connection and tables"""
    
    print("🔍 Debugging Database Connection...")
    print("=" * 50)
    
    # Check database settings
    print(f"Database Engine: {settings.DATABASES['default']['ENGINE']}")
    print(f"Database Name: {settings.DATABASES['default']['NAME']}")
    print(f"Database File Exists: {os.path.exists(settings.DATABASES['default']['NAME'])}")
    
    # Check if database file exists
    db_path = settings.DATABASES['default']['NAME']
    if os.path.exists(db_path):
        print(f"✅ Database file exists: {db_path}")
        print(f"   Size: {os.path.getsize(db_path)} bytes")
    else:
        print(f"❌ Database file does not exist: {db_path}")
    
    # Try to connect to database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"📊 Tables in database: {[table[0] for table in tables]}")
            
            if not tables:
                print("❌ No tables found in database!")
                print("🔧 Running migrations...")
                
                # Try to run migrations
                try:
                    execute_from_command_line(['manage.py', 'migrate'])
                    print("✅ Migrations completed successfully!")
                except Exception as e:
                    print(f"❌ Migration failed: {e}")
            else:
                print("✅ Database has tables - migrations appear to be working")
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("🔧 This might be why auth endpoints are failing")

if __name__ == "__main__":
    debug_database()
