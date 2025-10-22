#!/usr/bin/env python3
"""
Render startup script for Django backend
"""

import os
import sys
import subprocess
from django.core.management import execute_from_command_line

def main():
    print("🚀 Starting HackWestTX Backend on Render...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackwesttx.settings')
    
    try:
        # Run database migrations
        print("📊 Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Start the server with gunicorn
        print("🌐 Starting Gunicorn server...")
        port = os.environ.get('PORT', '8000')
        
        # Use subprocess to start gunicorn
        cmd = [
            'gunicorn',
            'hackwesttx.wsgi:application',
            '--bind', f'0.0.0.0:{port}',
            '--workers', '2',
            '--timeout', '120'
        ]
        
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd)
        
    except Exception as e:
        print(f"❌ Error during startup: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
