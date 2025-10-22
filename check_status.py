#!/usr/bin/env python3
"""
Check Backend Status
This script checks if your backend is up and running
"""

import requests
import json
import sys
import time

def check_backend_status(url):
    """Check if backend is running and show detailed status"""
    
    print("🔍 Checking Backend Status...")
    print("=" * 50)
    
    base_url = url.rstrip('/')
    
    try:
        # Check health endpoint
        print(f"🌐 Checking: {base_url}/api/health/")
        response = requests.get(f"{base_url}/api/health/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Backend is UP and running!")
            print(f"   Status: {data.get('status', 'Unknown')}")
            print(f"   Platform: {data.get('deployment', {}).get('platform', 'Unknown')}")
            print(f"   Environment: {data.get('deployment', {}).get('environment', 'Unknown')}")
            
            # Database status
            db_info = data.get('database', {})
            
            print("\n📊 Database Status:")
            
            # SQLite status
            sqlite = db_info.get('sqlite', {})
            sqlite_status = sqlite.get('status', 'unknown')
            if sqlite_status == 'connected':
                print(f"   ✅ SQLite: Connected ({len(sqlite.get('tables', []))} tables)")
            elif sqlite_status == 'no_tables':
                print(f"   ⚠️  SQLite: Connected but no tables (migrations needed)")
            else:
                print(f"   ❌ SQLite: {sqlite_status}")
            
            # MongoDB status
            mongodb = db_info.get('mongodb', {})
            mongodb_status = mongodb.get('status', 'unknown')
            if mongodb_status == 'connected':
                print(f"   ✅ MongoDB: Connected")
                collections = mongodb.get('collections', [])
                if collections:
                    print(f"      Collections: {', '.join(collections)}")
            elif mongodb_status == 'disabled':
                print(f"   ⚠️  MongoDB: Disabled")
            else:
                print(f"   ❌ MongoDB: {mongodb_status}")
                if 'error' in mongodb:
                    print(f"      Error: {mongodb['error']}")
            
            # Overall health
            overall_status = data.get('status', 'Unknown')
            if overall_status == 'OK':
                print("\n🎉 All systems operational!")
            elif overall_status == 'DEGRADED':
                print("\n⚠️  System is running but some components have issues")
            else:
                print("\n❌ System has critical issues")
            
            # Available endpoints
            endpoints = data.get('endpoints', {})
            if endpoints:
                print("\n🔗 Available Endpoints:")
                for name, url in endpoints.items():
                    if isinstance(url, dict):
                        print(f"   {name}:")
                        for sub_name, sub_url in url.items():
                            print(f"     - {sub_name}: {sub_url}")
                    else:
                        print(f"   {name}: {url}")
            
            return True
            
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   Make sure your backend is deployed and running")
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 check_status.py <backend-url>")
        print("Examples:")
        print("  python3 check_status.py https://your-app.onrender.com")
        print("  python3 check_status.py https://web-production-235d0.up.railway.app")
        sys.exit(1)
    
    url = sys.argv[1]
    success = check_backend_status(url)
    
    if success:
        print(f"\n✅ Your backend is running at: {url}")
        print("   You can now use it in your frontend application!")
    else:
        print(f"\n❌ Your backend is not accessible at: {url}")
        print("   Check your deployment logs and try again")

if __name__ == "__main__":
    main()
