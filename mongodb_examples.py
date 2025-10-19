#!/usr/bin/env python3
"""
MongoDB Atlas Request Examples
This script shows how to make various requests to your MongoDB Atlas database.
"""

from pymongo import MongoClient
from pymongo.server_api import ServerApi
import ssl
from datetime import datetime

# MongoDB Atlas connection string
uri = "mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def connect_to_mongodb():
    """Connect to MongoDB Atlas"""
    try:
        client = MongoClient(uri, server_api=ServerApi('1'), tlsAllowInvalidCertificates=True)
        client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas!")
        return client
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

def example_requests():
    """Example MongoDB requests"""
    client = connect_to_mongodb()
    if not client:
        return
    
    db = client['hackwesttx_db']
    
    # Example 1: Insert a document
    print("\n📝 Example 1: Insert a document")
    users_collection = db['users']
    user_doc = {
        "name": "John Doe",
        "email": "john@example.com",
        "created_at": datetime.now(),
        "preferences": {
            "theme": "dark",
            "notifications": True
        }
    }
    result = users_collection.insert_one(user_doc)
    print(f"✅ Inserted user with ID: {result.inserted_id}")
    
    # Example 2: Find documents
    print("\n🔍 Example 2: Find documents")
    users = users_collection.find({"email": "john@example.com"})
    for user in users:
        print(f"Found user: {user['name']} - {user['email']}")
    
    # Example 3: Update a document
    print("\n✏️ Example 3: Update a document")
    update_result = users_collection.update_one(
        {"email": "john@example.com"},
        {"$set": {"last_login": datetime.now()}}
    )
    print(f"✅ Updated {update_result.modified_count} document(s)")
    
    # Example 4: Create a calendar event
    print("\n📅 Example 4: Create a calendar event")
    events_collection = db['calendar_events']
    event_doc = {
        "title": "Study Session",
        "description": "Math homework review",
        "date": "2024-01-15",
        "time": "14:00",
        "user_id": result.inserted_id,
        "created_at": datetime.now()
    }
    event_result = events_collection.insert_one(event_doc)
    print(f"✅ Created event with ID: {event_result.inserted_id}")
    
    # Example 5: Find events for a user
    print("\n📋 Example 5: Find user's events")
    user_events = events_collection.find({"user_id": result.inserted_id})
    for event in user_events:
        print(f"Event: {event['title']} on {event['date']} at {event['time']}")
    
    # Example 6: Delete a document
    print("\n🗑️ Example 6: Delete a document")
    delete_result = users_collection.delete_one({"email": "john@example.com"})
    print(f"✅ Deleted {delete_result.deleted_count} document(s)")
    
    # Clean up events
    events_collection.delete_many({"user_id": result.inserted_id})
    print("✅ Cleaned up test data")
    
    client.close()
    print("\n🎉 All MongoDB requests completed successfully!")

if __name__ == "__main__":
    example_requests()
