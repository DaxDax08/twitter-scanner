#!/usr/bin/env python3
"""
Simple script to make your Twitter Scanner accessible from anywhere
Run this script to create a public tunnel
"""

import subprocess
import time
import sys
import os

def main():
    print("🌐 Twitter Scanner - Public Access Setup")
    print("=" * 50)
    
    print("📋 This will make your dashboard accessible from anywhere!")
    print("🔗 You'll get a public URL like: https://abc123.ngrok.io")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('app_telegram.py'):
        print("❌ app_telegram.py not found in current directory")
        print("📁 Please run this script from your twitter_scanner folder")
        input("Press Enter to exit...")
        return
    
    print("✅ Found Twitter Scanner app")
    
    # Method 1: Try ngrok
    print("\n🔍 Method 1: Using ngrok (Recommended)")
    print("📥 Download ngrok from: https://ngrok.com/download")
    print("📁 Extract ngrok.exe to this folder")
    print("🚀 Then run: ngrok http 5000")
    print()
    
    # Method 2: Alternative services
    print("🔍 Method 2: Alternative Services")
    print("🌐 Serveo (no installation): ssh -R 80:localhost:5000 serveo.net")
    print("🌐 localhost.run: ssh -R 80:localhost:5000 localhost.run")
    print("🌐 Cloudflare Tunnel: cloudflared tunnel --url http://localhost:5000")
    print()
    
    # Method 3: Manual instructions
    print("🔍 Method 3: Manual Setup")
    print("1. Start your app: python app_telegram.py")
    print("2. In another terminal, run one of the tunnel commands above")
    print("3. Copy the public URL and share it!")
    print()
    
    # Try to start the app
    print("🚀 Starting your Twitter Scanner...")
    try:
        print("📱 Your app will be available at: http://localhost:5000")
        print("🌐 To make it public, run a tunnel command in another terminal")
        print()
        print("Press Ctrl+C to stop the app")
        
        # Start the Flask app
        subprocess.run([sys.executable, 'app_telegram.py'])
        
    except KeyboardInterrupt:
        print("\n🛑 App stopped")
    except Exception as e:
        print(f"❌ Error starting app: {e}")

if __name__ == '__main__':
    main()
