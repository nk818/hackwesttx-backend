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
        enabled = getattr(settings, 'MONGODB_ENABLED', False)
        timeout = getattr(settings, 'MONGODB_TIMEOUT', 10) * 1000  # Convert to milliseconds
        
        if not uri or not enabled:
            return None
        
        # Use local MongoDB for development, Atlas for production
        if 'localhost' in uri or '127.0.0.1' in uri:
            # Local MongoDB - no SSL needed
            client = MongoClient(
                uri, 
                serverSelectionTimeoutMS=timeout,
                connectTimeoutMS=timeout
            )
        elif 'atlas-sql' in uri:
            # Atlas SQL endpoint - no Server API needed
            client = MongoClient(
                uri,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=timeout,
                connectTimeoutMS=timeout
            )
        else:
            # MongoDB Atlas - with SSL handling
            client = MongoClient(
                uri, 
                server_api=ServerApi('1'),
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=timeout,
                connectTimeoutMS=timeout,
                retryWrites=True,
                w='majority'
            )
        
        # Test connection
        client.admin.command('ping')
        return client
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None

def get_mongodb_database():
    """Get MongoDB database"""
    client = get_mongodb_client()
    if client is None:
        return None
    
    db_name = getattr(settings, 'MONGODB_DATABASE', 'hackwesttx_db')
    return client[db_name]

def store_additional_data(collection_name, data):
    """Store additional data in MongoDB"""
    if not getattr(settings, 'MONGODB_ENABLED', False):
        return None
    
    try:
        db = get_mongodb_database()
        if db is None:
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
        if db is None:
            return []
        
        collection = db[collection_name]
        if query:
            return list(collection.find(query))
        else:
            return list(collection.find())
    except Exception as e:
        print(f"Error retrieving data from MongoDB: {e}")
        return []

def test_mongodb_connection():
    """Test MongoDB connection and return status"""
    try:
        client = get_mongodb_client()
        if client is None:
            return {'status': 'failed', 'error': 'Client creation failed'}

        # Test connection
        client.admin.command('ping')

        # Test database access
        db = get_mongodb_database()
        if db is None:
            return {'status': 'failed', 'error': 'Database access failed'}

        # Test write/read
        test_collection = db['connection_test']
        test_doc = {'test': True, 'timestamp': '2025-10-28T02:20:00Z'}
        result = test_collection.insert_one(test_doc)

        # Clean up
        test_collection.delete_one({'_id': result.inserted_id})

        return {
            'status': 'success',
            'message': 'MongoDB connection successful',
            'database': getattr(settings, 'MONGODB_DATABASE', 'hackwesttx_db'),
            'enabled': getattr(settings, 'MONGODB_ENABLED', False)
        }

    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e),
            'enabled': getattr(settings, 'MONGODB_ENABLED', False)
        }