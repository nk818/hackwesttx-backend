"""
MongoDB utilities for additional data storage
"""
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from django.conf import settings

def get_mongodb_client():
    """Get MongoDB client connection"""
    try:
        uri = getattr(settings, 'MONGODB_URI', None)
        if not uri:
            return None
        
        client = MongoClient(
            uri, 
            server_api=ServerApi('1'),
            tlsAllowInvalidCertificates=True
        )
        return client
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None

def get_mongodb_database():
    """Get MongoDB database"""
    client = get_mongodb_client()
    if not client:
        return None
    
    db_name = getattr(settings, 'MONGODB_DATABASE', 'hackwesttx_db')
    return client[db_name]

def store_additional_data(collection_name, data):
    """Store additional data in MongoDB"""
    if not getattr(settings, 'MONGODB_ENABLED', False):
        return None
    
    try:
        db = get_mongodb_database()
        if not db:
            return None
        
        collection = db[collection_name]
        result = collection.insert_one(data)
        return result.inserted_id
    except Exception as e:
        print(f"Error storing data in MongoDB: {e}")
        return None

def get_additional_data(collection_name, query=None):
    """Retrieve additional data from MongoDB"""
    if not getattr(settings, 'MONGODB_ENABLED', False):
        return []
    
    try:
        db = get_mongodb_database()
        if not db:
            return []
        
        collection = db[collection_name]
        if query:
            return list(collection.find(query))
        else:
            return list(collection.find())
    except Exception as e:
        print(f"Error retrieving data from MongoDB: {e}")
        return []