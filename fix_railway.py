#!/usr/bin/env python3
"""
Fix Railway Deployment Script
This script will help you fix the crashed Railway deployment
"""

import os
import subprocess
import sys

def main():
    print("🔧 Fixing Railway Deployment")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app_telegram.py'):
        print("❌ app_telegram.py not found")
        print("📁 Please run this script from your twitter_scanner folder")
        return
    
    print("✅ Found Twitter Scanner files")
    
    # Create the fixed files
    print("\n🔧 Creating Railway-optimized files...")
    
    # Update requirements.txt for Railway
    railway_requirements = """flask==2.3.3
flask-sqlalchemy==3.0.5
flask-cors==4.0.0
requests==2.31.0
python-dotenv==1.0.0
beautifulsoup4==4.12.2
gunicorn==21.2.0
psycopg2-binary==2.9.7"""
    
    with open('requirements.txt', 'w') as f:
        f.write(railway_requirements)
    
    print("✅ Updated requirements.txt for Railway")
    
    # Create Railway configuration
    railway_config = """{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app_railway.py",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}"""
    
    with open('railway.json', 'w') as f:
        f.write(railway_config)
    
    print("✅ Created railway.json configuration")
    
    # Create Procfile
    with open('Procfile', 'w') as f:
        f.write('web: python app_railway.py\n')
    
    print("✅ Created Procfile")
    
    # Create .env template
    env_template = """# Railway Environment Variables
# Copy these to your Railway dashboard

SECRET_KEY=your-secret-key-here
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id

# Railway will automatically set:
# DATABASE_URL=postgresql://...
# PORT=5000
"""
    
    with open('.env.example', 'w') as f:
        f.write(env_template)
    
    print("✅ Created .env.example template")
    
    print("\n🎉 Railway Fix Complete!")
    print("=" * 50)
    print("📋 Next Steps:")
    print("1. Commit and push these changes to GitHub:")
    print("   git add .")
    print("   git commit -m 'Fix Railway deployment'")
    print("   git push")
    print()
    print("2. In Railway dashboard:")
    print("   - Go to your service settings")
    print("   - Add environment variables:")
    print("     SECRET_KEY=your-secret-key")
    print("     TELEGRAM_BOT_TOKEN=your-bot-token")
    print("     TELEGRAM_CHAT_ID=your-chat-id")
    print()
    print("3. Railway will automatically redeploy")
    print("4. Your app should now work!")
    print()
    print("🌐 Your dashboard will be accessible at:")
    print("   https://twitter-scanner-production.up.railway.app")

if __name__ == '__main__':
    main()
