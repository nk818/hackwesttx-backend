#!/usr/bin/env python3
"""
Complete build and setup script for Render deployment
Handles migrations, superuser creation, and static files
"""

import os
import sys
import subprocess
import django
from django.core.management import call_command
from django.contrib.auth import get_user_model

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def setup_django():
    """Set up Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()

def create_superuser():
    """Create superuser if environment variable is set"""
    if not os.environ.get('CREATE_SUPERUSER'):
        print("⏭️  Skipping superuser creation (CREATE_SUPERUSER not set)")
        return True
    
    print("👤 Creating superuser (triggered by CREATE_SUPERUSER env var)...")
    
    # Set environment variables for Django createsuperuser
    os.environ['DJANGO_SUPERUSER_USERNAME'] = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    os.environ['DJANGO_SUPERUSER_EMAIL'] = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@hackwesttx.com')
    os.environ['DJANGO_SUPERUSER_PASSWORD'] = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    
    try:
        call_command('createsuperuser', '--no-input')
        print(f"✅ Superuser created: {os.environ['DJANGO_SUPERUSER_USERNAME']}")
        return True
    except Exception as e:
        print(f"❌ Superuser creation failed: {e}")
        return False

def main():
    """Main build and setup process"""
    print("🚀 Starting HackWestTX Backend Build and Setup...")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("⚠️  Trying fallback requirements...")
        if not run_command("pip install -r requirements_minimal.txt", "Installing minimal dependencies"):
            print("❌ Failed to install dependencies")
            sys.exit(1)
    
    # Create necessary directories
    os.makedirs('staticfiles', exist_ok=True)
    
    # Ensure database file exists
    with open('db.sqlite3', 'a') as f:
        pass
    os.chmod('db.sqlite3', 0o664)
    
    # Set up Django
    setup_django()
    
    # Run migrations
    print("📊 Running Django migrations...")
    try:
        call_command('migrate', verbosity=2)
        print("✅ Migrations completed successfully")
    except Exception as e:
        print(f"❌ Migrations failed: {e}")
        sys.exit(1)
    
    # Create superuser
    if not create_superuser():
        print("❌ Superuser creation failed")
        sys.exit(1)
    
    # Collect static files
    print("📁 Collecting static files...")
    try:
        call_command('collectstatic', '--noinput', verbosity=2)
        print("✅ Static files collected successfully")
    except Exception as e:
        print(f"❌ Static file collection failed: {e}")
        sys.exit(1)
    
    print("🎉 Build and setup completed successfully!")

if __name__ == '__main__':
    main()
