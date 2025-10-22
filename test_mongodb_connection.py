#!/usr/bin/env python3
"""
Test MongoDB Atlas connection
"""

import os
import sys
from pymongo import MongoClient
from pymongo.server_api import ServerApi

def main():
    print("🔍 Testing MongoDB Atlas connection...")
    
    try:
        # Get MongoDB URI
        uri = os.environ.get('MONGODB_URI', 'mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        print(f"📊 Connecting to: {uri[:50]}...")
        
        # Create client
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB Atlas connection successful!")
        
        # List databases
        databases = client.list_database_names()
        print(f"📊 Available databases: {databases}")
        
        # Test hackwesttx database
        db = client['hackwesttx']
        collections = db.list_collection_names()
        print(f"📊 Collections in hackwesttx: {collections}")
        
        # Close connection
        client.close()
        print("🎉 MongoDB Atlas test completed successfully!")
        
    except Exception as e:
        print(f"❌ MongoDB Atlas connection failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
