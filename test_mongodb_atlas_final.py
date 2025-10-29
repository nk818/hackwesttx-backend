#!/usr/bin/env python3
"""
Test MongoDB Atlas connection with proper configuration
This script verifies that MongoDB Atlas is properly configured and working.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
django.setup()

from django.conf import settings
from api.mongodb_utils import get_mongodb_client, get_mongodb_database, test_mongodb_connection
from pymongo import MongoClient
from pymongo.server_api import ServerApi

def test_connection():
    """Test MongoDB Atlas connection"""
    print("🔍 Testing MongoDB Atlas Connection...")
    print("=" * 60)
    
    # Check configuration
    print("\n📋 Configuration Check:")
    print(f"   MONGODB_URI: {'✅ Set' if settings.MONGODB_URI else '❌ Not set'}")
    if settings.MONGODB_URI:
        # Hide credentials in output
        uri_display = settings.MONGODB_URI.split('@')[1] if '@' in settings.MONGODB_URI else '***'
        print(f"   URI: mongodb+srv://***@{uri_display}")
    print(f"   MONGODB_DATABASE: {settings.MONGODB_DATABASE}")
    print(f"   MONGODB_ENABLED: {'✅ Yes' if settings.MONGODB_ENABLED else '❌ No'}")
    print(f"   MONGODB_TIMEOUT: {settings.MONGODB_TIMEOUT} seconds")
    
    if not settings.MONGODB_ENABLED:
        print("\n❌ MongoDB is disabled in settings")
        return False
    
    # Test using mongodb_utils
    print("\n🧪 Testing via mongodb_utils:")
    result = test_mongodb_connection()
    print(f"   Status: {'✅ Success' if result['status'] == 'success' else '❌ Failed'}")
    if result['status'] == 'success':
        print(f"   Message: {result.get('message', 'N/A')}")
        print(f"   Database: {result.get('database', 'N/A')}")
    else:
        print(f"   Error: {result.get('error', 'Unknown error')}")
        return False
    
    # Test direct connection
    print("\n🧪 Testing direct pymongo connection:")
    try:
        client = get_mongodb_client()
        if client is None:
            print("   ❌ Failed to create client")
            return False
        
        print("   ✅ Client created successfully")
        
        # Test database access
        db = get_mongodb_database()
        if db is None:
            print("   ❌ Failed to access database")
            return False
        
        print(f"   ✅ Database '{settings.MONGODB_DATABASE}' accessed successfully")
        
        # List collections
        collections = db.list_collection_names()
        print(f"   📊 Found {len(collections)} collections")
        if collections:
            print(f"      Collections: {', '.join(collections[:5])}" + ('...' if len(collections) > 5 else ''))
        
        # Test write operation
        test_collection = db['connection_test']
        test_doc = {
            'test': True,
            'source': 'test_mongodb_atlas_final',
            'timestamp': '2025-01-28T00:00:00Z'
        }
        result = test_collection.insert_one(test_doc)
        print(f"   ✅ Write test successful - Document ID: {result.inserted_id}")
        
        # Test read operation
        retrieved_doc = test_collection.find_one({'_id': result.inserted_id})
        if retrieved_doc:
            print("   ✅ Read test successful")
        else:
            print("   ❌ Read test failed")
            return False
        
        # Clean up
        test_collection.delete_one({'_id': result.inserted_id})
        print("   🧹 Test document cleaned up")
        
        client.close()
        print("\n🎉 All MongoDB Atlas tests passed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)

