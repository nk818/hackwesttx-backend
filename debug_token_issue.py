#!/usr/bin/env python3
"""
Debug token and authentication issues
"""

import os
import sys
import django
from django.conf import settings
from django.db import connection
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import requests
import json

def debug_token_issue():
    """Debug token and authentication issues"""
    print("🔍 Token and Authentication Debug")
    print("=" * 50)
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    django.setup()
    
    try:
        User = get_user_model()
        
        # 1. Check database tables
        print("\n📊 Database Tables Check:")
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"   Total tables: {len(tables)}")
            
            # Check for auth tables
            auth_tables = ['auth_user', 'api_user', 'authtoken_token']
            for table in auth_tables:
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
                if cursor.fetchone():
                    print(f"   ✅ {table} exists")
                else:
                    print(f"   ❌ {table} missing")
        
        # 2. Check users in database
        print("\n👥 Users in Database:")
        try:
            users = User.objects.all()
            print(f"   Total users: {users.count()}")
            for user in users:
                print(f"   - {user.username} (ID: {user.id}, Superuser: {user.is_superuser})")
        except Exception as e:
            print(f"   ❌ Error getting users: {e}")
        
        # 3. Check tokens
        print("\n🔑 Tokens in Database:")
        try:
            tokens = Token.objects.all()
            print(f"   Total tokens: {tokens.count()}")
            for token in tokens:
                print(f"   - User: {token.user.username}, Key: {token.key[:10]}...")
        except Exception as e:
            print(f"   ❌ Error getting tokens: {e}")
        
        # 4. Test login endpoint
        print("\n🌐 Testing Login Endpoint:")
        try:
            # Test with a test user
            test_username = "testuser"
            test_password = "testpass123"
            
            # Create test user if doesn't exist
            if not User.objects.filter(username=test_username).exists():
                print(f"   Creating test user: {test_username}")
                User.objects.create_user(
                    username=test_username,
                    email="test@example.com",
                    password=test_password
                )
            
            # Test login
            login_data = {
                "username": test_username,
                "password": test_password
            }
            
            response = requests.post(
                "https://hackwesttx-backend.onrender.com/api/auth/login/",
                json=login_data,
                timeout=10
            )
            
            print(f"   Login response status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Login successful")
                print(f"   Token: {data.get('token', 'No token')[:20]}...")
                print(f"   User: {data.get('user', {}).get('username', 'No user')}")
            else:
                print(f"   ❌ Login failed: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Login test failed: {e}")
        
        # 5. Check token persistence
        print("\n💾 Token Persistence Test:")
        try:
            # Get a user and their token
            user = User.objects.first()
            if user:
                token, created = Token.objects.get_or_create(user=user)
                print(f"   User: {user.username}")
                print(f"   Token: {token.key}")
                print(f"   Token created: {created}")
                
                # Test if token works for authentication
                headers = {"Authorization": f"Token {token.key}"}
                response = requests.get(
                    "https://hackwesttx-backend.onrender.com/api/auth/me/",
                    headers=headers,
                    timeout=10
                )
                print(f"   Token auth status: {response.status_code}")
                if response.status_code == 200:
                    print("   ✅ Token authentication works")
                else:
                    print("   ❌ Token authentication failed")
            else:
                print("   ❌ No users found")
                
        except Exception as e:
            print(f"   ❌ Token persistence test failed: {e}")
        
        # 6. Check database file permissions
        print("\n📁 Database File Check:")
        db_path = settings.DATABASES['default']['NAME']
        if os.path.exists(db_path):
            stat = os.stat(db_path)
            print(f"   Database file exists: {db_path}")
            print(f"   File size: {stat.st_size} bytes")
            print(f"   Permissions: {oct(stat.st_mode)}")
        else:
            print(f"   ❌ Database file not found: {db_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    debug_token_issue()
