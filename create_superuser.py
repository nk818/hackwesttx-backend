#!/usr/bin/env python3
"""
Create superuser for Django admin
Run this script to create a superuser account
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    print("🔧 Creating Django Superuser...")
    
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("✅ Superuser already exists!")
        superuser = User.objects.filter(is_superuser=True).first()
        print(f"   Username: {superuser.username}")
        print(f"   Email: {superuser.email}")
        return
    
    # Create superuser
    try:
        user = User.objects.create_superuser(
            username='admin',
            email='admin@hackwesttx.com',
            password='admin123'
        )
        print("✅ Superuser created successfully!")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Email: admin@hackwesttx.com")
        print("\n🌐 You can now access Django admin at:")
        print("   https://your-app-name.onrender.com/admin/")
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
