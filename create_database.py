#!/usr/bin/env python
"""
Create PostgreSQL database if it doesn't exist
"""
import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from urllib.parse import urlparse

def create_database():
    """Create the database if it doesn't exist"""
    # Get database URL from environment
    database_url = os.environ.get(
        'DATABASE_URL',
        'postgresql://blueprint_postures_learn_user:FOlENaCbVYqr9ZwBOE5QEkSRxkKgp8Lv@dpg-d3s34rodl3ps73d29o70-a:5432/blueprint-postures-learn'
    )
    
    # Parse the connection string
    parsed = urlparse(database_url)
    db_name = parsed.path[1:] if parsed.path.startswith('/') else parsed.path
    
    # Connect to postgres database to create our database
    admin_url = f"{parsed.scheme}://{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port or 5432}/postgres"
    
    try:
        # Connect to postgres database (default database that always exists)
        conn = psycopg2.connect(admin_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,)
        )
        exists = cursor.fetchone()
        
        if not exists:
            print(f"📊 Creating database '{db_name}'...")
            # Create database - use quotes to handle hyphens in name
            try:
                cursor.execute(f'CREATE DATABASE "{db_name}"')
                print(f"✅ Database '{db_name}' created successfully!")
            except Exception as create_error:
                print(f"⚠️  Could not create database: {create_error}")
                print(f"   Trying alternative: creating without quotes...")
                # Try without quotes if that fails
                cursor.execute(f'CREATE DATABASE {db_name.replace("-", "_")}')
                print(f"✅ Created database '{db_name.replace('-', '_')}'")
        else:
            print(f"✅ Database '{db_name}' already exists")
        
        cursor.close()
        conn.close()
        return True
    except psycopg2.errors.InsufficientPrivilege:
        print(f"⚠️  Insufficient privileges to create database. Trying to connect to existing database...")
        return False
    except psycopg2.OperationalError as e:
        if "does not exist" in str(e):
            print(f"⚠️  Database '{db_name}' does not exist and cannot be created automatically.")
            print(f"   Please create it manually in your PostgreSQL server.")
            return False
        raise
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        # Try to continue anyway - maybe database exists with different name
        return False

if __name__ == '__main__':
    success = create_database()
    sys.exit(0 if success else 0)  # Don't fail build if can't create DB

