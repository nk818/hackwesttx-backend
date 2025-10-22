#!/usr/bin/env python3
"""
Test Authentication Endpoints
This script tests all authentication-related endpoints on your Railway deployment
"""

import requests
import json
import sys

def test_auth_endpoints(railway_url):
    """Test authentication endpoints"""
    
    print("🔐 Testing Authentication Endpoints...")
    print("=" * 50)
    
    base_url = railway_url.rstrip('/')
    
    # Test endpoints
    auth_endpoints = [
        ("/api/auth/register/", "POST", "User Registration"),
        ("/api/auth/login/", "POST", "User Login"),
        ("/api/auth/me/", "GET", "Get Current User"),
        ("/api/auth/request-password-reset/", "POST", "Request Password Reset"),
        ("/api/health/", "GET", "Health Check")
    ]
    
    results = {}
    
    for endpoint, method, description in auth_endpoints:
        try:
            url = f"{base_url}{endpoint}"
            print(f"\n🔍 Testing {description}: {method} {url}")
            
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                # Test with sample data for POST endpoints
                if "register" in endpoint:
                    test_data = {
                        "username": "testuser",
                        "email": "test@example.com",
                        "password": "testpassword123",
                        "first_name": "Test",
                        "last_name": "User"
                    }
                elif "login" in endpoint:
                    test_data = {
                        "username": "testuser",
                        "password": "testpassword123"
                    }
                elif "password-reset" in endpoint:
                    test_data = {
                        "email": "test@example.com"
                    }
                else:
                    test_data = {}
                
                response = requests.post(url, json=test_data, timeout=10)
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code in [200, 201]:
                print(f"✅ {description}: OK ({response.status_code})")
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)[:300]}...")
                except:
                    print(f"   Response: {response.text[:300]}...")
                results[endpoint] = f"SUCCESS ({response.status_code})"
            elif response.status_code == 404:
                print(f"❌ {description}: ENDPOINT NOT FOUND (404)")
                print(f"   Error: {response.text[:200]}")
                results[endpoint] = "ENDPOINT NOT FOUND (404)"
            elif response.status_code == 405:
                print(f"⚠️  {description}: METHOD NOT ALLOWED (405)")
                print(f"   This endpoint exists but doesn't support {method}")
                results[endpoint] = f"METHOD NOT ALLOWED (405)"
            else:
                print(f"❌ {description}: FAILED ({response.status_code})")
                print(f"   Error: {response.text[:200]}")
                results[endpoint] = f"FAILED ({response.status_code})"
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: CONNECTION ERROR")
            print(f"   Error: {e}")
            results[endpoint] = f"CONNECTION ERROR: {e}"
    
    # Test API Root to see all available endpoints
    print(f"\n🔍 Testing API Root: GET {base_url}/")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ API Root: OK")
            print("📋 Available Auth Endpoints:")
            if 'endpoints' in data and 'auth' in data['endpoints']:
                for auth_endpoint, details in data['endpoints']['auth'].items():
                    print(f"   - {auth_endpoint}: {details}")
            else:
                print("   - No auth endpoints found in API root")
        else:
            print(f"❌ API Root: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ API Root: ERROR - {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 AUTHENTICATION TEST SUMMARY")
    print("=" * 50)
    
    for endpoint, status in results.items():
        status_icon = "✅" if "SUCCESS" in status else "❌" if "FAILED" in status or "CONNECTION ERROR" in status else "⚠️"
        print(f"{status_icon} {endpoint}: {status}")
    
    success_count = sum(1 for status in results.values() if "SUCCESS" in status)
    total_count = len(results)
    
    print(f"\n🎯 Success Rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("🎉 All authentication endpoints are working!")
    elif success_count > 0:
        print("⚠️  Some authentication endpoints are working.")
        print("   Check the failed ones above for issues.")
    else:
        print("❌ No authentication endpoints are accessible.")
        print("   Check your Railway deployment and API configuration.")
    
    return results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 test_auth_endpoints.py <railway-url>")
        print("Example: python3 test_auth_endpoints.py https://web-production-235d0.up.railway.app")
        sys.exit(1)
    
    railway_url = sys.argv[1]
    test_auth_endpoints(railway_url)
