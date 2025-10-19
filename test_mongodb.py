#!/usr/bin/env python3
"""
Simple MongoDB Atlas Connection Test
This script tests your MongoDB Atlas connection without any Django integration.
"""

from pymongo import MongoClient
from pymongo.server_api import ServerApi

# MongoDB Atlas connection string
uri = "mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

print("🔍 Testing MongoDB Atlas Connection...")
print("=" * 50)

try:
    # Create a new client and connect to the server
    import ssl
    client = MongoClient(uri, server_api=ServerApi('1'), tlsAllowInvalidCertificates=True)
    
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("✅ Pinged your deployment. You successfully connected to MongoDB!")
    
    # Test database operations
    db = client['hackwesttx_db']
    print(f"✅ Connected to database: {db.name}")
    
    # List collections
    collections = db.list_collection_names()
    print(f"📊 Available collections: {collections}")
    
    # Test inserting a document
    test_collection = db['test_collection']
    test_doc = {
        "message": "Hello from HackWestTX!",
        "timestamp": "2024-01-01T00:00:00Z",
        "test": True
    }
    
    result = test_collection.insert_one(test_doc)
    print(f"✅ Inserted test document with ID: {result.inserted_id}")
    
    # Test reading the document
    retrieved_doc = test_collection.find_one({"_id": result.inserted_id})
    print(f"✅ Retrieved document: {retrieved_doc}")
    
    # Clean up test document
    test_collection.delete_one({"_id": result.inserted_id})
    print("✅ Cleaned up test document")
    
    print("\n🎉 MongoDB Atlas connection is working perfectly!")
    print("You can now use this connection string in your applications.")
    
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")
    print("\nTroubleshooting tips:")
    print("1. Check if your IP address is whitelisted in MongoDB Atlas")
    print("2. Verify your database user has proper permissions")
    print("3. Check your network connection")
    print("4. Ensure your password is correct in the connection string")
