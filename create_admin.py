#!/usr/bin/env python3
"""
Simple script to create admin superuser
"""

import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_admin():
    """Create admin superuser"""
    User = get_user_model()
    
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("✅ Superuser already exists!")
        return True
    
    try:
        # Create superuser
        User.objects.create_superuser(
            username='admin',
            email='admin@hackwesttx.com',
            password='admin123'
        )
        print("✅ Superuser 'admin' created successfully!")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Email: admin@hackwesttx.com")
        return True
    except Exception as e:
        print(f"❌ Failed to create superuser: {e}")
        return False

if __name__ == '__main__':
    success = create_admin()
    if not success:
        sys.exit(1)
