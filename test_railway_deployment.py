#!/usr/bin/env python3
"""
Test Railway Deployment
This script tests your deployed Railway backend.
"""

import requests
import json
from datetime import datetime

def test_railway_backend(base_url):
    """Test the deployed Railway backend"""
    
    print(f"🧪 Testing Railway Backend: {base_url}")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/api/health/", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: API Root
    print("\n2️⃣ Testing API Root...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ API root accessible!")
            data = response.json()
            print(f"API Version: {data.get('version', 'Unknown')}")
            print(f"Available endpoints: {len(data.get('endpoints', {}))}")
        else:
            print(f"❌ API root failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API root error: {e}")
    
    # Test 3: Calendar Events
    print("\n3️⃣ Testing Calendar Events...")
    try:
        response = requests.get(f"{base_url}/api/calendar-events/", timeout=10)
        if response.status_code in [200, 401, 403]:  # 401/403 is expected without auth
            print("✅ Calendar events endpoint accessible!")
            if response.status_code == 200:
                events = response.json()
                print(f"Found {len(events)} events")
            else:
                print("Authentication required (expected)")
        else:
            print(f"❌ Calendar events failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Calendar events error: {e}")
    
    # Test 4: User Registration
    print("\n4️⃣ Testing User Registration...")
    try:
        user_data = {
            "username": f"testuser_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "email": f"test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = requests.post(f"{base_url}/api/auth/register/", json=user_data, timeout=10)
        if response.status_code == 201:
            print("✅ User registration working!")
            user_info = response.json()
            print(f"User created: {user_info.get('username', 'Unknown')}")
        elif response.status_code == 400:
            print("⚠️ Registration endpoint working (validation error expected)")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Registration error: {e}")
    
    print("\n🎉 Railway Backend Testing Complete!")
    print(f"Your backend is live at: {base_url}")

if __name__ == "__main__":
    # Replace with your actual Railway URL
    RAILWAY_URL = "https://hackwesttx-backend-production.railway.app"
    
    print("🚀 Railway Backend Test Suite")
    print("=" * 60)
    print(f"Testing URL: {RAILWAY_URL}")
    print("=" * 60)
    
    test_railway_backend(RAILWAY_URL)
    
    print("\n💡 If tests fail, check:")
    print("1. Railway deployment is complete")
    print("2. Environment variables are set correctly")
    print("3. MongoDB connection is working")
    print("4. No errors in Railway logs")
