#!/usr/bin/env python3
"""
Debug Railway Deployment
This script helps debug Railway deployment issues.
"""

import os
import sys

print("🔍 Railway Debug Information")
print("=" * 50)

# Check environment variables
print("\n📋 Environment Variables:")
print(f"PORT: {os.environ.get('PORT', 'NOT SET')}")
print(f"RAILWAY_ENVIRONMENT: {os.environ.get('RAILWAY_ENVIRONMENT', 'NOT SET')}")
print(f"RAILWAY_PROJECT_ID: {os.environ.get('RAILWAY_PROJECT_ID', 'NOT SET')}")
print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'NOT SET')}")
print(f"DEBUG: {os.environ.get('DEBUG', 'NOT SET')}")

# Check if we're on Railway
is_railway = (
    os.environ.get('RAILWAY_ENVIRONMENT') or 
    os.environ.get('RAILWAY_PROJECT_ID') or 
    os.environ.get('PORT')
)

print(f"\n🚀 Railway Detection: {'YES' if is_railway else 'NO'}")

# Check Python version
print(f"\n🐍 Python Version: {sys.version}")

# Check current working directory
print(f"\n📁 Current Directory: {os.getcwd()}")

# Check if manage.py exists
manage_py_exists = os.path.exists('manage.py')
print(f"\n📄 manage.py exists: {'YES' if manage_py_exists else 'NO'}")

# Check if settings.py exists
settings_exists = os.path.exists('hackwesttx/settings.py')
print(f"📄 settings.py exists: {'YES' if settings_exists else 'NO'}")

print("\n" + "=" * 50)
print("🎯 If you see this output, Python is working on Railway!")
print("🎯 If Django isn't starting, check the logs for errors.")
