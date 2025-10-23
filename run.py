#!/usr/bin/env python3
"""
Twitter Scanner Startup Script
Run this to start the Twitter scanner application
"""

import os
import sys
from app import app, db

def main():
    """Main startup function"""
    print("🐦 Starting Twitter Scanner...")
    print("=" * 50)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")
    
    # Check for environment variables
    required_vars = ['SECRET_KEY']
    optional_vars = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER', 
                     'USER_PHONE_NUMBER', 'PUSHBULLET_ACCESS_TOKEN']
    
    missing_required = [var for var in required_vars if not os.getenv(var)]
    missing_optional = [var for var in optional_vars if not os.getenv(var)]
    
    if missing_required:
        print("❌ Missing required environment variables:")
        for var in missing_required:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file or environment")
        sys.exit(1)
    
    if missing_optional:
        print("⚠️  Optional notification services not configured:")
        for var in missing_optional:
            print(f"   - {var}")
        print("   (Notifications will be disabled)")
    
    print("\n🚀 Starting web server...")
    print("📱 Open your browser to: http://localhost:5000")
    print("🔄 Background monitoring will start automatically")
    print("=" * 50)
    
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()

