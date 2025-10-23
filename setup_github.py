#!/usr/bin/env python3
"""
GitHub Setup Script for Twitter Scanner
This will help you deploy your Twitter Scanner to GitHub and get a public URL
"""

import os
import subprocess
import sys

def check_git():
    """Check if git is installed"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except:
        return False

def init_git_repo():
    """Initialize git repository"""
    print("🔧 Setting up Git repository...")
    
    # Initialize git
    subprocess.run(['git', 'init'], check=True)
    print("✅ Git repository initialized")
    
    # Add all files
    subprocess.run(['git', 'add', '.'], check=True)
    print("✅ Files added to git")
    
    # Initial commit
    subprocess.run(['git', 'commit', '-m', 'Initial commit: Twitter Scanner'], check=True)
    print("✅ Initial commit created")

def create_github_repo_instructions():
    """Create instructions for GitHub repository"""
    instructions = """
# 🐙 GitHub Repository Setup Instructions

## Step 1: Create GitHub Repository
1. Go to https://github.com
2. Click "New repository"
3. Name it: `twitter-scanner`
4. Make it public (for free hosting)
5. Don't initialize with README (we already have one)
6. Click "Create repository"

## Step 2: Connect Local Repository
Run these commands in your terminal:

```bash
git remote add origin https://github.com/YOUR_USERNAME/twitter-scanner.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Free Hosting

### Option A: Railway.app (Recommended)
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your `twitter-scanner` repository
5. Railway will automatically deploy your app
6. You'll get a public URL like: `https://twitter-scanner-production.up.railway.app`

### Option B: Render.com
1. Go to https://render.com
2. Sign up with GitHub
3. Create new "Web Service"
4. Connect your GitHub repository
5. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app_telegram.py`
6. Deploy and get your public URL

### Option C: Vercel (Serverless)
1. Go to https://vercel.com
2. Import your GitHub repository
3. Vercel will automatically detect Python
4. Deploy and get your public URL

## Step 4: Set Environment Variables
In your hosting platform, add these environment variables:
- `SECRET_KEY`: Your Flask secret key
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID

## Step 5: Access Your Dashboard
Once deployed, your dashboard will be accessible from:
- ✅ Any computer
- ✅ Any phone or tablet
- ✅ From anywhere in the world
- ✅ No network restrictions

## 🔄 Auto-Deploy
Every time you push code to GitHub:
- Your app automatically redeploys
- Updates are live within minutes
- No manual deployment needed

## 📱 Mobile Access
Your dashboard works perfectly on:
- 📱 iPhones and Android phones
- 📱 Tablets and iPads
- 💻 Windows, Mac, and Linux computers
- 🌐 Any web browser

## 🎉 You're Done!
Your Twitter Scanner is now live and accessible from anywhere!
"""
    
    with open('GITHUB_SETUP.md', 'w') as f:
        f.write(instructions)
    
    print("✅ Created GitHub setup instructions")

def main():
    """Main setup function"""
    print("🐙 GitHub Deployment Setup for Twitter Scanner")
    print("=" * 60)
    
    if not check_git():
        print("❌ Git not found. Please install Git first:")
        print("📥 Download from: https://git-scm.com/downloads")
        return
    
    print("✅ Git is installed")
    
    # Check if we're in the right directory
    if not os.path.exists('app_telegram.py'):
        print("❌ app_telegram.py not found")
        print("📁 Please run this script from your twitter_scanner folder")
        return
    
    print("✅ Found Twitter Scanner files")
    
    # Initialize git repository
    try:
        init_git_repo()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error setting up git: {e}")
        return
    
    # Create setup instructions
    create_github_repo_instructions()
    
    print("\n🎉 GitHub Setup Complete!")
    print("=" * 60)
    print("📋 Next Steps:")
    print("1. Read GITHUB_SETUP.md for detailed instructions")
    print("2. Create a GitHub repository")
    print("3. Push your code to GitHub")
    print("4. Deploy to free hosting (Railway, Render, or Vercel)")
    print("5. Get your public URL!")
    print()
    print("🌐 Your dashboard will be accessible from anywhere!")
    print("📱 Works on phones, tablets, and computers worldwide!")

if __name__ == '__main__':
    main()

