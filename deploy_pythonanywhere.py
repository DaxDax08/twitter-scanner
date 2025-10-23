#!/usr/bin/env python3
"""
PythonAnywhere deployment script
Run this on PythonAnywhere to set up your Twitter Scanner
"""

import os
import sys
import subprocess

def setup_pythonanywhere():
    """Set up the Twitter Scanner on PythonAnywhere"""
    print("🐍 Setting up Twitter Scanner on PythonAnywhere...")
    print("=" * 50)
    
    # Install dependencies
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    
    # Create database
    print("🗄️  Setting up database...")
    try:
        from app_render import app, db
        with app.app_context():
            db.create_all()
        print("✅ Database created")
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False
    
    print("🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Go to your PythonAnywhere dashboard")
    print("2. Create a new web app")
    print("3. Choose 'Manual configuration'")
    print("4. Set the source code to your project directory")
    print("5. Set the WSGI file to: app_render.py")
    print("6. Add your environment variables in the web app settings")
    
    return True

if __name__ == "__main__":
    setup_pythonanywhere()
