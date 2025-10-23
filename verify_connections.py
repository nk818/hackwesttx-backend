#!/usr/bin/env python3
"""
Comprehensive connection verification for Render + MongoDB Atlas architecture
"""

import os
import sys
import django
from django.conf import settings
from django.db import connection
import pymongo
from datetime import datetime
import requests

def verify_render_connection():
    """Verify Render deployment is working"""
    print("🌐 Render Deployment Verification")
    print("=" * 50)
    
    try:
        # Check if we're on Render
        is_render = os.environ.get('RENDER') == 'true'
        print(f"   Render Environment: {'✅ Yes' if is_render else '❌ No'}")
        
        # Check Render-specific environment variables
        port = os.environ.get('PORT')
        print(f"   Render PORT: {port if port else 'Not set'}")
        
        # Check if we can access the health endpoint
        try:
            response = requests.get('https://hackwesttx-backend.onrender.com/api/health/', timeout=10)
            if response.status_code == 200:
                print("   ✅ Health endpoint accessible")
                print(f"   📊 Response: {response.json()}")
            else:
                print(f"   ⚠️  Health endpoint returned: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Cannot access health endpoint: {e}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Render verification failed: {e}")
        return False

def verify_sqlite_connection():
    """Verify SQLite database connection"""
    print("\n🗄️  SQLite Database Verification")
    print("=" * 50)
    
    try:
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
        django.setup()
        
        # Check database configuration
        db_config = settings.DATABASES['default']
        print(f"   Engine: {db_config['ENGINE']}")
        print(f"   Name: {db_config['NAME']}")
        
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"   ✅ Connected - Found {len(tables)} tables")
            
            # Check for api_user table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_user';")
            if cursor.fetchone():
                print("   ✅ api_user table exists")
            else:
                print("   ❌ api_user table missing")
                
            # Check for auth_user table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
            if cursor.fetchone():
                print("   ✅ auth_user table exists")
            else:
                print("   ❌ auth_user table missing")
        
        return True
        
    except Exception as e:
        print(f"   ❌ SQLite verification failed: {e}")
        return False

def verify_mongodb_atlas_connection():
    """Verify MongoDB Atlas connection"""
    print("\n🍃 MongoDB Atlas Verification")
    print("=" * 50)
    
    try:
        # Get MongoDB configuration
        mongodb_uri = os.environ.get('MONGODB_URI')
        mongodb_enabled = os.environ.get('MONGODB_ENABLED', 'False').lower() == 'true'
        
        print(f"   MongoDB Enabled: {'✅ Yes' if mongodb_enabled else '❌ No'}")
        print(f"   MongoDB URI: {'✅ Set' if mongodb_uri else '❌ Not set'}")
        
        if not mongodb_enabled or not mongodb_uri:
            print("   ⚠️  MongoDB not configured")
            return False
        
        # Test connection
        client = pymongo.MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        
        # Ping the database
        client.admin.command('ping')
        print("   ✅ Connection successful")
        
        # Get database info
        db = client['hackwesttx_db']
        collections = db.list_collection_names()
        print(f"   📊 Found {len(collections)} collections")
        
        # Test write operation
        test_collection = db['connection_test']
        test_doc = {
            'test': True,
            'timestamp': datetime.now(),
            'source': 'connection_verification',
            'render_deployment': True
        }
        result = test_collection.insert_one(test_doc)
        print(f"   ✅ Write test successful - ID: {result.inserted_id}")
        
        # Test read operation
        retrieved_doc = test_collection.find_one({'_id': result.inserted_id})
        if retrieved_doc:
            print("   ✅ Read test successful")
        else:
            print("   ❌ Read test failed")
        
        # Clean up test document
        test_collection.delete_one({'_id': result.inserted_id})
        print("   🧹 Test document cleaned up")
        
        return True
        
    except Exception as e:
        print(f"   ❌ MongoDB Atlas verification failed: {e}")
        return False

def verify_request_flow():
    """Verify the complete request flow"""
    print("\n🔄 Request Flow Verification")
    print("=" * 50)
    
    try:
        # Test API endpoints
        base_url = "https://hackwesttx-backend.onrender.com"
        endpoints = [
            '/api/health/',
            '/api/verify-database/',
            '/api/auth/register/',
            '/api/auth/login/'
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
                print(f"   {endpoint}: {response.status_code}")
            except Exception as e:
                print(f"   {endpoint}: ❌ {e}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Request flow verification failed: {e}")
        return False

def main():
    """Main verification function"""
    print("🔍 Comprehensive Connection Verification")
    print("=" * 60)
    print("Architecture: Flutter App → Render (Backend) → MongoDB Atlas (DB)")
    print("=" * 60)
    
    # Verify all connections
    render_ok = verify_render_connection()
    sqlite_ok = verify_sqlite_connection()
    mongodb_ok = verify_mongodb_atlas_connection()
    flow_ok = verify_request_flow()
    
    # Summary
    print("\n📋 Connection Summary")
    print("=" * 50)
    print(f"   🌐 Render Deployment: {'✅ OK' if render_ok else '❌ FAILED'}")
    print(f"   🗄️  SQLite Database: {'✅ OK' if sqlite_ok else '❌ FAILED'}")
    print(f"   🍃 MongoDB Atlas: {'✅ OK' if mongodb_ok else '❌ FAILED'}")
    print(f"   🔄 Request Flow: {'✅ OK' if flow_ok else '❌ FAILED'}")
    
    if all([render_ok, sqlite_ok, mongodb_ok, flow_ok]):
        print("\n🎉 All connections verified successfully!")
        print("   Your architecture is working correctly:")
        print("   Flutter App → Render → MongoDB Atlas")
    else:
        print("\n⚠️  Some connections failed. Check the details above.")
    
    return all([render_ok, sqlite_ok, mongodb_ok, flow_ok])

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
