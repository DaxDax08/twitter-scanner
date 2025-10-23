#!/usr/bin/env python3
"""
Setup script for making the Twitter Scanner accessible from anywhere
This script will:
1. Install ngrok if not present
2. Configure the app for external access
3. Start the tunnel
"""

import os
import sys
import subprocess
import time
import requests
import threading
from pathlib import Path

def check_ngrok_installed():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ngrok():
    """Install ngrok"""
    print("📥 Installing ngrok...")
    
    # Download ngrok for Windows
    ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
    
    try:
        import urllib.request
        import zipfile
        
        print("Downloading ngrok...")
        urllib.request.urlretrieve(ngrok_url, "ngrok.zip")
        
        print("Extracting ngrok...")
        with zipfile.ZipFile("ngrok.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Clean up
        os.remove("ngrok.zip")
        
        print("✅ ngrok installed successfully!")
        return True
    except Exception as e:
        print(f"❌ Error installing ngrok: {e}")
        return False

def start_ngrok_tunnel(port=5000):
    """Start ngrok tunnel"""
    print(f"🌐 Starting ngrok tunnel on port {port}...")
    
    try:
        # Start ngrok in background
        process = subprocess.Popen(['ngrok', 'http', str(port)], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
        
        # Wait a moment for ngrok to start
        time.sleep(3)
        
        # Get the public URL
        try:
            response = requests.get('http://localhost:4040/api/tunnels')
            if response.status_code == 200:
                tunnels = response.json()['tunnels']
                if tunnels:
                    public_url = tunnels[0]['public_url']
                    print(f"✅ Public URL: {public_url}")
                    print(f"🔗 You can now access your dashboard from anywhere using this link!")
                    return public_url, process
        except:
            pass
        
        print("⚠️  ngrok started but couldn't get public URL automatically")
        print("📱 Check the ngrok web interface at: http://localhost:4040")
        return None, process
        
    except Exception as e:
        print(f"❌ Error starting ngrok: {e}")
        return None, None

def update_app_config():
    """Update app configuration for external access"""
    print("🔧 Updating app configuration for external access...")
    
    # Read the current app file
    with open('app_telegram.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the host configuration
    old_config = "app.run(debug=True, host='127.0.0.1', port=5000)"
    new_config = "app.run(debug=True, host='0.0.0.0', port=5000)"
    
    if old_config in content:
        content = content.replace(old_config, new_config)
        
        # Write back the updated content
        with open('app_telegram.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ App configuration updated for external access")
        return True
    else:
        print("⚠️  App configuration already set for external access")
        return True

def create_start_script():
    """Create a start script that runs both the app and ngrok"""
    script_content = '''@echo off
echo Starting Twitter Scanner with Public Access...
echo.

REM Start the Python app in background
start "Twitter Scanner" python app_telegram.py

REM Wait a moment for the app to start
timeout /t 5 /nobreak >nul

REM Start ngrok tunnel
echo Starting public tunnel...
ngrok http 5000

echo.
echo Press any key to stop both the app and tunnel...
pause >nul

REM Kill the Python process
taskkill /f /im python.exe >nul 2>&1
'''
    
    with open('start_public.bat', 'w') as f:
        f.write(script_content)
    
    print("✅ Created start_public.bat script")

def main():
    """Main setup function"""
    print("🌐 Twitter Scanner - Public Access Setup")
    print("=" * 50)
    
    # Check if ngrok is installed
    if not check_ngrok_installed():
        print("📥 ngrok not found. Installing...")
        if not install_ngrok():
            print("❌ Failed to install ngrok. Please install manually from: https://ngrok.com/download")
            return
    else:
        print("✅ ngrok is already installed")
    
    # Update app configuration
    update_app_config()
    
    # Create start script
    create_start_script()
    
    print("\n" + "=" * 50)
    print("🚀 Setup Complete!")
    print("=" * 50)
    print("📋 To start your public dashboard:")
    print("   1. Run: start_public.bat")
    print("   2. Or manually: python app_telegram.py (in one terminal)")
    print("   3. Then: ngrok http 5000 (in another terminal)")
    print()
    print("🌐 Once started, you'll get a public URL like:")
    print("   https://abc123.ngrok.io")
    print("   Share this URL to access from anywhere!")
    print()
    print("⚠️  Security Note: This makes your dashboard public.")
    print("   Consider adding authentication if needed.")
    print("=" * 50)

if __name__ == '__main__':
    main()

