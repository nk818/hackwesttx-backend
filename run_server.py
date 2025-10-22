#!/usr/bin/env python3
"""
Railway Server Runner
This script ensures migrations run before starting the Django server
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Run migrations and start Django server"""
    
    print("🚀 Starting Railway deployment...")
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    print("📊 Running database migrations...")
    
    # Run migrations
    try:
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        print("✅ Migrations completed successfully!")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        # Continue anyway - the server might still work
    
    print("🌐 Starting Django server...")
    
    # Start the server
    port = os.environ.get('PORT', '8080')
    execute_from_command_line(['manage.py', 'runserver', f'0.0.0.0:{port}'])

if __name__ == '__main__':
    main()
