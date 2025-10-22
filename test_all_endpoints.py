#!/usr/bin/env python3
"""
Test All Endpoints on Railway Deployment
This script tests various endpoints to see what's working
"""

import requests
import json
import sys

def test_all_endpoints(railway_url):
    """Test all available endpoints"""
    
    print("🔍 Testing All Endpoints on Railway...")
    print("=" * 60)
    
    base_url = railway_url.rstrip('/')
    
    # Test various endpoint categories
    endpoints = [
        # Basic endpoints
        ("/", "GET", "API Root"),
        ("/debug/", "GET", "Debug Info"),
        ("/api/health/", "GET", "Health Check"),
        
        # Auth endpoints
        ("/api/auth/register/", "POST", "User Registration"),
        ("/api/auth/login/", "POST", "User Login"),
        ("/api/auth/me/", "GET", "Get Current User"),
        ("/api/auth/request-password-reset/", "POST", "Request Password Reset"),
        
        # API endpoints
        ("/api/", "GET", "API Endpoints List"),
        ("/api/departments/", "GET", "Departments List"),
        ("/api/professors/", "GET", "Professors List"),
        ("/api/portfolios/", "GET", "Portfolios List"),
        ("/api/courses/", "GET", "Courses List"),
        ("/api/materials/", "GET", "Materials List"),
        ("/api/flashcards/", "GET", "Flashcards List"),
        ("/api/quizzes/", "GET", "Quizzes List"),
        ("/api/important-dates/", "GET", "Important Dates List"),
        ("/api/reviews/", "GET", "Reviews List"),
        ("/api/study-groups/", "GET", "Study Groups List"),
        ("/api/notifications/", "GET", "Notifications List"),
        ("/api/posts/", "GET", "Posts List"),
        ("/api/users/", "GET", "Users List"),
        
        # Search endpoints
        ("/api/search/", "GET", "Global Search"),
        ("/api/visitor/landing/", "GET", "Visitor Landing"),
        ("/api/visitor/search/", "GET", "Visitor Search"),
        
        # Admin endpoints
        ("/admin/", "GET", "Django Admin"),
    ]
    
    results = {}
    
    for endpoint, method, description in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            print(f"\n🔍 Testing {description}: {method} {url}")
            
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                # Test with minimal data for POST endpoints
                test_data = {
                    "username": "testuser",
                    "email": "test@example.com",
                    "password": "testpass123"
                }
                response = requests.post(url, json=test_data, timeout=10)
            
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
    
    # Summary by category
    print("\n" + "=" * 60)
    print("📊 ENDPOINT TEST SUMMARY")
    print("=" * 60)
    
    # Categorize results
    categories = {
        "Basic Endpoints": ["/", "/debug/", "/api/health/"],
        "Auth Endpoints": ["/api/auth/register/", "/api/auth/login/", "/api/auth/me/", "/api/auth/request-password-reset/"],
        "API Endpoints": ["/api/", "/api/departments/", "/api/professors/", "/api/portfolios/", "/api/courses/", "/api/materials/", "/api/flashcards/", "/api/quizzes/", "/api/important-dates/", "/api/reviews/", "/api/study-groups/", "/api/notifications/", "/api/posts/", "/api/users/"],
        "Search Endpoints": ["/api/search/", "/api/visitor/landing/", "/api/visitor/search/"],
        "Admin Endpoints": ["/admin/"]
    }
    
    for category, endpoints_list in categories.items():
        print(f"\n📋 {category}:")
        for endpoint in endpoints_list:
            if endpoint in results:
                status = results[endpoint]
                if "SUCCESS" in status:
                    icon = "✅"
                elif "AUTH_REQUIRED" in status:
                    icon = "⚠️"
                elif "NOT_FOUND" in status:
                    icon = "❌"
                elif "SERVER_ERROR" in status:
                    icon = "❌"
                else:
                    icon = "❌"
                print(f"   {icon} {endpoint}: {status}")
    
    # Overall statistics
    success_count = sum(1 for status in results.values() if "SUCCESS" in status)
    auth_required_count = sum(1 for status in results.values() if "AUTH_REQUIRED" in status)
    not_found_count = sum(1 for status in results.values() if "NOT_FOUND" in status)
    server_error_count = sum(1 for status in results.values() if "SERVER_ERROR" in status)
    total_count = len(results)
    
    print(f"\n🎯 Overall Statistics:")
    print(f"   ✅ Working: {success_count}")
    print(f"   ⚠️  Auth Required: {auth_required_count}")
    print(f"   ❌ Not Found: {not_found_count}")
    print(f"   ❌ Server Error: {server_error_count}")
    print(f"   📊 Total: {total_count}")
    
    if success_count > 0:
        print(f"\n🎉 {success_count} endpoints are working!")
        if auth_required_count > 0:
            print(f"   ⚠️  {auth_required_count} endpoints require authentication")
        if server_error_count > 0:
            print(f"   ❌ {server_error_count} endpoints have server errors (likely database issues)")
    else:
        print("❌ No endpoints are working properly")
    
    return results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 test_all_endpoints.py <railway-url>")
        print("Example: python3 test_all_endpoints.py https://web-production-235d0.up.railway.app")
        sys.exit(1)
    
    railway_url = sys.argv[1]
    test_all_endpoints(railway_url)
