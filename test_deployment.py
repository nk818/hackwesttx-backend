#!/usr/bin/env python3
"""
Test Railway Deployment - No CLI Required
This script tests your Railway deployment endpoints directly
"""

import requests
import json
import sys

def test_railway_deployment():
    """Test Railway deployment endpoints"""
    
    print("🚀 Testing Railway Deployment...")
    print("=" * 50)
    
    # You need to replace this with your actual Railway URL
    # Get it from your Railway dashboard
    railway_url = input("Enter your Railway app URL (e.g., https://your-app.railway.app): ").strip()
    
    if not railway_url:
        print("❌ No URL provided. Exiting.")
        return
    
    if not railway_url.startswith('http'):
        railway_url = f"https://{railway_url}"
    
    # Test endpoints
    endpoints = [
        ("/", "API Root"),
        ("/debug/", "Debug Info"),
        ("/api/health/", "Health Check"),
        ("/api/", "API Endpoints")
    ]
    
    results = {}
    
    for endpoint, description in endpoints:
        try:
            url = f"{railway_url.rstrip('/')}{endpoint}"
            print(f"\n🔍 Testing {description}: {url}")
            
            response = requests.get(url, timeout=10)
            
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
    print("📊 DEPLOYMENT TEST SUMMARY")
    print("=" * 50)
    
    for endpoint, status in results.items():
        status_icon = "✅" if status == "SUCCESS" else "❌"
        print(f"{status_icon} {endpoint}: {status}")
    
    success_count = sum(1 for status in results.values() if status == "SUCCESS")
    total_count = len(results)
    
    print(f"\n🎯 Success Rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("🎉 All endpoints are working! Your Railway deployment is successful!")
    elif success_count > 0:
        print("⚠️  Some endpoints are working. Check the failed ones above.")
    else:
        print("❌ No endpoints are accessible. Check your Railway deployment.")
        print("\n🔧 Troubleshooting:")
        print("1. Check Railway dashboard for deployment status")
        print("2. Set environment variables in Railway dashboard")
        print("3. Check Railway logs for errors")
    
    return results

if __name__ == "__main__":
    test_railway_deployment()
