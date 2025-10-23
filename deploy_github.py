#!/usr/bin/env python3
"""
GitHub Deployment Setup for Twitter Scanner
This script will help you deploy your Twitter Scanner to GitHub
"""

import os
import json
import subprocess
import sys

def create_github_repo():
    """Create GitHub repository setup"""
    print("🐙 Setting up GitHub deployment for Twitter Scanner")
    print("=" * 60)
    
    # Check if git is installed
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        print("✅ Git is installed")
    except:
        print("❌ Git not found. Please install Git first: https://git-scm.com/downloads")
        return False
    
    return True

def create_github_actions():
    """Create GitHub Actions workflow for deployment"""
    os.makedirs('.github/workflows', exist_ok=True)
    
    workflow_content = '''name: Deploy Twitter Scanner

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Deploy to Railway
      uses: railway-app/railway-deploy@v1
      with:
        railway-token: ${{ secrets.RAILWAY_TOKEN }}
        service: twitter-scanner
'''
    
    with open('.github/workflows/deploy.yml', 'w') as f:
        f.write(workflow_content)
    
    print("✅ Created GitHub Actions workflow")

def create_railway_config():
    """Create Railway.app configuration"""
    railway_config = {
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "python app_telegram.py",
            "healthcheckPath": "/",
            "healthcheckTimeout": 100
        }
    }
    
    with open('railway.json', 'w') as f:
        json.dump(railway_config, f, indent=2)
    
    print("✅ Created Railway configuration")

def create_heroku_config():
    """Create Heroku configuration"""
    with open('Procfile', 'w') as f:
        f.write('web: python app_telegram.py\n')
    
    print("✅ Created Heroku Procfile")

def create_render_config():
    """Create Render.com configuration"""
    render_config = {
        "services": [
            {
                "name": "twitter-scanner",
                "type": "web",
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "python app_telegram.py",
                "envVars": [
                    {
                        "key": "SECRET_KEY",
                        "value": "your-secret-key-here"
                    }
                ]
            }
        ]
    }
    
    with open('render.yaml', 'w') as f:
        import yaml
        yaml.dump(render_config, f, default_flow_style=False)
    
    print("✅ Created Render configuration")

def create_vercel_config():
    """Create Vercel configuration for serverless deployment"""
    vercel_config = {
        "version": 2,
        "builds": [
            {
                "src": "app_telegram.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "app_telegram.py"
            }
        ]
    }
    
    with open('vercel.json', 'w') as f:
        json.dump(vercel_config, f, indent=2)
    
    print("✅ Created Vercel configuration")

def create_deployment_guide():
    """Create deployment guide"""
    guide_content = '''# Twitter Scanner - GitHub Deployment Guide

## 🚀 Free Hosting Options

### Option 1: Railway.app (Recommended)
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your twitter-scanner repository
5. Railway will automatically deploy your app
6. You'll get a public URL like: https://twitter-scanner-production.up.railway.app

### Option 2: Render.com
1. Go to https://render.com
2. Sign up with GitHub
3. Create new "Web Service"
4. Connect your GitHub repository
5. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app_telegram.py`
6. Deploy and get your public URL

### Option 3: Heroku
1. Install Heroku CLI
2. Run: `heroku create your-app-name`
3. Run: `git push heroku main`
4. Your app will be live at: https://your-app-name.herokuapp.com

### Option 4: Vercel (Serverless)
1. Go to https://vercel.com
2. Import your GitHub repository
3. Vercel will automatically detect Python
4. Deploy and get your public URL

## 🔧 Environment Variables

Set these in your hosting platform:
- `SECRET_KEY`: Your Flask secret key
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID

## 📱 Access Your Dashboard

Once deployed, your dashboard will be accessible from:
- Any computer
- Any phone
- Any tablet
- From anywhere in the world!

## 🔄 Auto-Deploy

With GitHub Actions, every time you push code:
- Your app automatically redeploys
- Updates are live within minutes
- No manual deployment needed

## 🛡️ Security

For production use, consider:
- Adding authentication
- Using environment variables for secrets
- Setting up proper database backups
'''
    
    with open('DEPLOYMENT_GUIDE.md', 'w') as f:
        f.write(guide_content)
    
    print("✅ Created deployment guide")

def main():
    """Main setup function"""
    print("🐙 GitHub Deployment Setup for Twitter Scanner")
    print("=" * 60)
    
    if not create_github_repo():
        return
    
    print("\n📋 Creating deployment configurations...")
    
    # Create all deployment configs
    create_github_actions()
    create_railway_config()
    create_heroku_config()
    create_render_config()
    create_vercel_config()
    create_deployment_guide()
    
    print("\n🎉 Setup Complete!")
    print("=" * 60)
    print("📋 Next Steps:")
    print("1. Initialize git: git init")
    print("2. Add files: git add .")
    print("3. Commit: git commit -m 'Initial commit'")
    print("4. Create GitHub repo and push")
    print("5. Choose a hosting platform from DEPLOYMENT_GUIDE.md")
    print("6. Deploy and get your public URL!")
    print()
    print("🌐 Your dashboard will be accessible from anywhere!")
    print("📱 Works on phones, tablets, and computers worldwide!")

if __name__ == '__main__':
    main()
