#!/usr/bin/env python3
"""
Simple script to create a public tunnel for the Twitter Scanner
This will make your dashboard accessible from anywhere on the internet
"""

import subprocess
import time
import requests
import threading
import webbrowser
from pathlib import Path

def check_ngrok():
    """Check if ngrok is available"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ngrok_simple():
    """Simple ngrok installation"""
    print("📥 Setting up ngrok...")
    
    # Try to download ngrok
    try:
        import urllib.request
        import zipfile
        
        print("Downloading ngrok...")
        ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
        urllib.request.urlretrieve(ngrok_url, "ngrok.zip")
        
        print("Extracting ngrok...")
        with zipfile.ZipFile("ngrok.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Clean up
        Path("ngrok.zip").unlink()
        
        print("✅ ngrok ready!")
        return True
    except Exception as e:
        print(f"❌ Error setting up ngrok: {e}")
        return False

def start_tunnel():
    """Start the public tunnel"""
    print("🌐 Creating public tunnel...")
    
    try:
        # Start ngrok
        process = subprocess.Popen(['ngrok', 'http', '5000'], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
        
        # Wait for ngrok to start
        time.sleep(3)
        
        # Get the public URL
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            if response.status_code == 200:
                tunnels = response.json()['tunnels']
                if tunnels:
                    public_url = tunnels[0]['public_url']
                    print(f"\n🎉 SUCCESS! Your dashboard is now public!")
                    print(f"🔗 Public URL: {public_url}")
                    print(f"📱 Share this link to access from anywhere!")
                    print(f"🌍 Works on phones, tablets, and other computers!")
                    
                    # Try to open the URL
                    try:
                        webbrowser.open(public_url)
                        print("🚀 Opening dashboard in your browser...")
                    except:
                        pass
                    
                    return public_url, process
        except:
            pass
        
        print("⚠️  Tunnel started but couldn't get URL automatically")
        print("📱 Check: http://localhost:4040 for the public URL")
        return None, process
        
    except Exception as e:
        print(f"❌ Error starting tunnel: {e}")
        return None, None

def main():
    """Main function"""
    print("🌐 Twitter Scanner - Public Access")
    print("=" * 50)
    
    # Check if ngrok exists
    if not check_ngrok():
        print("📥 ngrok not found. Setting up...")
        if not install_ngrok_simple():
            print("\n❌ Failed to set up ngrok automatically.")
            print("📋 Manual setup:")
            print("1. Download ngrok from: https://ngrok.com/download")
            print("2. Extract ngrok.exe to this folder")
            print("3. Run this script again")
            return
    
    print("🚀 Starting your app and creating public tunnel...")
    print("⏳ This may take a moment...")
    
    # Start the tunnel
    public_url, process = start_tunnel()
    
    if public_url:
        print(f"\n✅ Dashboard is live at: {public_url}")
        print("📱 You can now access it from any device!")
        print("\n⚠️  Press Ctrl+C to stop the tunnel")
        
        try:
            # Keep running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping tunnel...")
            if process:
                process.terminate()
            print("✅ Tunnel stopped")
    else:
        print("❌ Failed to create public tunnel")
        print("📋 Try running: ngrok http 5000")

if __name__ == '__main__':
    main()
