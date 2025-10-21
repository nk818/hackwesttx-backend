"""
MongoDB utilities for Django integration
"""
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from django.conf import settings
import ssl

def get_mongodb_client():
    """Get MongoDB client connection"""
    try:
        uri = settings.MONGODB_URI
        client = MongoClient(
            uri, 
            server_api=ServerApi('1'), 
            tlsAllowInvalidCertificates=True
        )
        # Test the connection
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
            return {'status': 'failed', 'error': 'Could not create client'}
    except Exception as e:
        return {'status': 'failed', 'error': str(e)}
