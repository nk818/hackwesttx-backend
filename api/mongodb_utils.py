"""
MongoDB utilities for Django integration
"""
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from django.conf import settings
import ssl
import time

def get_mongodb_client():
    """Get MongoDB client connection with timeout and error handling"""
    # Check if MongoDB is enabled
    if not getattr(settings, 'MONGODB_ENABLED', False):
        return None
        
    try:
        uri = settings.MONGODB_URI
        client = MongoClient(
            uri, 
            server_api=ServerApi('1'), 
            tlsAllowInvalidCertificates=True,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
        # Test the connection with timeout
        client.admin.command('ping')
        return client
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None

def get_mongodb_database():
    """Get MongoDB database instance"""
    client = get_mongodb_client()
    if client:
        return client['hackwesttx_db']
    return None

def test_mongodb_connection():
    """Test MongoDB connection and return status"""
    # Check if MongoDB is enabled
    if not getattr(settings, 'MONGODB_ENABLED', False):
        return {'status': 'disabled', 'message': 'MongoDB is disabled in settings'}
        
    try:
        client = get_mongodb_client()
        if client:
            # Test basic operations
            db = client['hackwesttx_db']
            collections = db.list_collection_names()
            return {
                'status': 'connected',
                'database': 'hackwesttx_db',
                'collections': collections
            }
        else:
            return {'status': 'failed', 'error': 'Could not create client - SSL or network issue'}
    except Exception as e:
        return {'status': 'failed', 'error': str(e)[:100]}

def is_mongodb_available():
    """Check if MongoDB is available and working"""
    return test_mongodb_connection().get('status') == 'connected'
