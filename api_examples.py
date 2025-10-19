#!/usr/bin/env python3
"""
Django Backend API Request Examples
This script shows how to make HTTP requests to your Django backend API.
"""

import requests
import json
from datetime import datetime

# Base URL for your Django backend
BASE_URL = "http://localhost:8000/api"

def make_api_request(method, endpoint, data=None, headers=None):
    """Make an API request to the Django backend"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        print(f"📡 {method} {url}")
        print(f"Status: {response.status_code}")
        
        if response.status_code < 400:
            print("✅ Success!")
            if response.content:
                try:
                    return response.json()
                except:
                    return response.text
        else:
            print(f"❌ Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure your Django server is running!")
        print("Run: python manage.py runserver")
        return None
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def example_api_requests():
    """Example API requests to Django backend"""
    
    print("🚀 Django Backend API Request Examples")
    print("=" * 50)
    
    # Example 1: Health check
    print("\n1️⃣ Health Check")
    health = make_api_request("GET", "/health/")
    if health:
        print(f"Response: {health}")
    
    # Example 2: Get API root
    print("\n2️⃣ API Root")
    api_root = make_api_request("GET", "/")
    if api_root:
        print(f"API Version: {api_root.get('version', 'Unknown')}")
        print(f"Available endpoints: {len(api_root.get('endpoints', {}))}")
    
    # Example 3: Register a new user
    print("\n3️⃣ User Registration")
    user_data = {
        "username": "testuser123",
        "email": "testuser123@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    register_response = make_api_request("POST", "/auth/register/", user_data)
    if register_response:
        print(f"User registered: {register_response.get('username', 'Unknown')}")
        user_id = register_response.get('id')
    else:
        print("Registration failed or user already exists")
        user_id = None
    
    # Example 4: Login
    print("\n4️⃣ User Login")
    login_data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    login_response = make_api_request("POST", "/auth/login/", login_data)
    if login_response:
        token = login_response.get('token')
        print(f"Login successful! Token: {token[:20]}...")
        headers = {"Authorization": f"Token {token}"}
    else:
        print("Login failed")
        headers = None
    
    # Example 5: Get user profile (requires authentication)
    if headers:
        print("\n5️⃣ Get User Profile")
        profile = make_api_request("GET", "/auth/me/", headers=headers)
        if profile:
            print(f"User: {profile.get('username', 'Unknown')}")
            print(f"Email: {profile.get('email', 'Unknown')}")
    
    # Example 6: Create a calendar event (requires authentication)
    if headers:
        print("\n6️⃣ Create Calendar Event")
        event_data = {
            "title": "Study Session",
            "description": "Math homework review",
            "date": "2024-01-15",
            "time": "14:00",
            "event_type": "study",
            "priority": "high"
        }
        event_response = make_api_request("POST", "/calendar-events/create/", event_data, headers)
        if event_response:
            print(f"Event created: {event_response.get('title', 'Unknown')}")
            event_id = event_response.get('id')
        else:
            event_id = None
    
    # Example 7: Get user's calendar events
    if headers:
        print("\n7️⃣ Get User's Calendar Events")
        events = make_api_request("GET", "/calendar-events/user/", headers=headers)
        if events:
            print(f"Found {len(events)} events")
            for event in events[:3]:  # Show first 3 events
                print(f"  - {event.get('title', 'No title')} on {event.get('date', 'No date')}")
    
    # Example 8: Get departments
    print("\n8️⃣ Get Departments")
    departments = make_api_request("GET", "/departments/")
    if departments:
        print(f"Found {len(departments)} departments")
        for dept in departments[:3]:  # Show first 3 departments
            print(f"  - {dept.get('name', 'No name')} ({dept.get('code', 'No code')})")
    
    # Example 9: Search portfolios
    print("\n9️⃣ Search Portfolios")
    search_params = "?search=math&limit=5"
    portfolios = make_api_request("GET", f"/portfolios/{search_params}")
    if portfolios:
        print(f"Found {len(portfolios)} portfolios")
        for portfolio in portfolios[:3]:  # Show first 3 portfolios
            print(f"  - {portfolio.get('title', 'No title')} by {portfolio.get('professor', 'Unknown')}")
    
    print("\n🎉 All API requests completed!")
    print("\n💡 To run your Django server:")
    print("   python manage.py runserver")
    print("\n💡 To test MongoDB connection:")
    print("   python3 test_mongodb.py")

if __name__ == "__main__":
    example_api_requests()
