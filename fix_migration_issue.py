#!/usr/bin/env python3
"""
Fix the migration issue with custom User model
"""

import os
import sys
import django
from django.core.management import call_command
from django.db import connection

def fix_migration_issue():
    """Fix the migration issue"""
    print("🔧 Fixing Migration Issue...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        # Check current migration state
        print("📊 Checking current migration state...")
        call_command('showmigrations', 'api', verbosity=2)
        
        # Delete problematic migrations
        print("🗑️  Removing problematic migrations...")
        migration_files = [
            'api/migrations/0001_initial.py',
            'api/migrations/0002_user.py'
        ]
        
        for migration_file in migration_files:
            if os.path.exists(migration_file):
                os.remove(migration_file)
                print(f"✅ Removed {migration_file}")
        
        # Reset all migrations
        print("🔄 Resetting all migrations...")
        call_command('migrate', 'api', 'zero', verbosity=2)
        
        # Create fresh initial migration
        print("📊 Creating fresh initial migration...")
        call_command('makemigrations', 'api', verbosity=2)
        
        # Apply migrations
        print("📊 Applying fresh migrations...")
        call_command('migrate', 'api', verbosity=2)
        
        # Create superuser
        from api.models import User
        if not User.objects.filter(is_superuser=True).exists():
            print("👤 Creating superuser...")
            User.objects.create_superuser(
                username='admin',
                email='admin@hackwesttx.com',
                password='admin123'
            )
            print("✅ Superuser created: admin/admin123")
        else:
            print("✅ Superuser already exists")
        
        print("✅ Migration issue fixed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to fix migration issue: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = fix_migration_issue()
    if not success:
        sys.exit(1)
