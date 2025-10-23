#!/usr/bin/env python3
"""
Simple superuser creation script
Run this to create a superuser for your Django app
"""

import os
import sys
import django
from django.contrib.auth import get_user_model

def create_superuser():
    """Create a superuser if it doesn't exist"""
    print("👤 Creating superuser...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    User = get_user_model()
    
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("✅ Superuser already exists!")
        existing_superuser = User.objects.filter(is_superuser=True).first()
        print(f"   Username: {existing_superuser.username}")
        print(f"   Email: {existing_superuser.email}")
        return True
    
    try:
        # Create superuser
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@hackwesttx.com',
            password='admin123'
        )
        print("✅ Superuser created successfully!")
        print(f"   Username: {superuser.username}")
        print(f"   Email: {superuser.email}")
        print(f"   Password: admin123")
        return True
    except Exception as e:
        print(f"❌ Failed to create superuser: {e}")
        return False

if __name__ == '__main__':
    success = create_superuser()
    if not success:
        sys.exit(1)
