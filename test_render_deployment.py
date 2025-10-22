#!/usr/bin/env python3
"""
Test Render Deployment
This script tests your Render deployment endpoints
"""

import requests
import json
import sys

def test_render_deployment(render_url):
    """Test Render deployment endpoints"""
    
    print("🚀 Testing Render Deployment...")
    print("=" * 50)
    
    base_url = render_url.rstrip('/')
    
    # Test endpoints
    endpoints = [
        ("/", "GET", "API Root"),
        ("/debug/", "GET", "Debug Info"),
        ("/api/health/", "GET", "Health Check"),
        ("/api/", "GET", "API Endpoints"),
        ("/api/auth/register/", "POST", "User Registration"),
        ("/api/auth/login/", "POST", "User Login"),
        ("/api/departments/", "GET", "Departments List"),
        ("/api/professors/", "GET", "Professors List"),
        ("/api/portfolios/", "GET", "Portfolios List"),
        ("/admin/", "GET", "Django Admin"),
    ]
    
    results = {}
    
    for endpoint, method, description in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            print(f"\n🔍 Testing {description}: {method} {url}")
            
            if method == "GET":
                response = requests.get(url, timeout=15)
            elif method == "POST":
                test_data = {
                    "username": "testuser",
                    "email": "test@example.com",
                    "password": "testpass123"
                }
                response = requests.post(url, json=test_data, timeout=15)
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ {description}: OK (200)")
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)[:150]}...")
                except:
                    print(f"   Response: {response.text[:150]}...")
                results[endpoint] = "SUCCESS (200)"
            elif response.status_code == 201:
                print(f"✅ {description}: CREATED (201)")
                results[endpoint] = "SUCCESS (201)"
            elif response.status_code == 403:
                print(f"⚠️  {description}: FORBIDDEN (403) - Authentication required")
                results[endpoint] = "AUTH_REQUIRED (403)"
            elif response.status_code == 404:
                print(f"❌ {description}: NOT FOUND (404)")
                results[endpoint] = "NOT_FOUND (404)"
            elif response.status_code == 500:
                print(f"❌ {description}: SERVER ERROR (500)")
                print(f"   Error: {response.text[:100]}...")
                results[endpoint] = "SERVER_ERROR (500)"
            else:
                print(f"❌ {description}: FAILED ({response.status_code})")
                print(f"   Error: {response.text[:100]}...")
                results[endpoint] = f"FAILED ({response.status_code})"
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: CONNECTION ERROR")
            print(f"   Error: {e}")
            results[endpoint] = f"CONNECTION_ERROR: {e}"
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 RENDER DEPLOYMENT TEST SUMMARY")
    print("=" * 50)
    
    for endpoint, status in results.items():
        if "SUCCESS" in status:
            icon = "✅"
        elif "AUTH_REQUIRED" in status:
            icon = "⚠️"
        elif "NOT_FOUND" in status or "SERVER_ERROR" in status:
            icon = "❌"
        else:
            icon = "❌"
        print(f"{icon} {endpoint}: {status}")
    
    success_count = sum(1 for status in results.values() if "SUCCESS" in status)
    auth_required_count = sum(1 for status in results.values() if "AUTH_REQUIRED" in status)
    error_count = sum(1 for status in results.values() if "SERVER_ERROR" in status or "NOT_FOUND" in status)
    total_count = len(results)
    
    print(f"\n🎯 Statistics:")
    print(f"   ✅ Working: {success_count}")
    print(f"   ⚠️  Auth Required: {auth_required_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📊 Total: {total_count}")
    
    if success_count >= 4:  # At least basic endpoints working
        print(f"\n🎉 Render deployment is working!")
        print(f"   Your backend is ready at: {base_url}")
        if auth_required_count > 0:
            print(f"   ⚠️  {auth_required_count} endpoints require authentication (normal)")
        if error_count > 0:
            print(f"   ❌ {error_count} endpoints have issues (check database connection)")
    else:
        print("❌ Render deployment has issues")
        print("   Check your deployment logs and environment variables")
    
    return results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 test_render_deployment.py <render-url>")
        print("Example: python3 test_render_deployment.py https://hackwesttx-backend.onrender.com")
        sys.exit(1)
    
    render_url = sys.argv[1]
    test_render_deployment(render_url)
