#!/usr/bin/env python3
"""
Simple Auth Test - Test basic functionality without database
"""

import requests
import json

def test_simple_endpoints(railway_url):
    """Test simple endpoints that don't require database"""
    
    print("🧪 Testing Simple Endpoints...")
    print("=" * 50)
    
    base_url = railway_url.rstrip('/')
    
    # Test endpoints that should work without database
    simple_endpoints = [
        ("/", "API Root"),
        ("/debug/", "Debug Info"),
        ("/api/health/", "Health Check"),
    ]
    
    results = {}
    
    for endpoint, description in simple_endpoints:
        try:
            url = f"{base_url}{endpoint}"
            print(f"\n🔍 Testing {description}: {url}")
            
            response = requests.get(url, timeout=10)
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ {description}: OK (200)")
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
                results[endpoint] = "SUCCESS"
            else:
                print(f"❌ {description}: FAILED ({response.status_code})")
                print(f"   Error: {response.text[:200]}")
                results[endpoint] = f"FAILED ({response.status_code})"
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: CONNECTION ERROR")
            print(f"   Error: {e}")
            results[endpoint] = f"CONNECTION ERROR: {e}"
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SIMPLE ENDPOINTS TEST SUMMARY")
    print("=" * 50)
    
    for endpoint, status in results.items():
        status_icon = "✅" if "SUCCESS" in status else "❌"
        print(f"{status_icon} {endpoint}: {status}")
    
    success_count = sum(1 for status in results.values() if "SUCCESS" in status)
    total_count = len(results)
    
    print(f"\n🎯 Success Rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("🎉 All simple endpoints are working!")
        print("   The issue is specifically with database-dependent endpoints.")
    else:
        print("❌ Some basic endpoints are not working.")
    
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 test_simple_auth.py <railway-url>")
        print("Example: python3 test_simple_auth.py https://web-production-235d0.up.railway.app")
        sys.exit(1)
    
    railway_url = sys.argv[1]
    test_simple_endpoints(railway_url)
