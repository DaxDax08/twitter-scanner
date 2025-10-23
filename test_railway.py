#!/usr/bin/env python3
"""
Test script to verify Railway deployment configuration
"""

import os
import sys

def test_import():
    """Test if the app can be imported correctly"""
    try:
        print("🧪 Testing Railway app import...")
        
        # Set environment variables for testing
        os.environ['SECRET_KEY'] = 'test-secret-key'
        os.environ['PORT'] = '5000'
        
        # Try to import the app
        from app_railway import app
        print("✅ App imported successfully")
        
        # Test if app is a Flask instance
        if hasattr(app, 'route'):
            print("✅ Flask app is properly configured")
        else:
            print("❌ App is not a Flask instance")
            return False
            
        print("✅ Railway configuration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def main():
    print("🧪 Railway Deployment Test")
    print("=" * 40)
    
    if test_import():
        print("\n🎉 All tests passed!")
        print("✅ Your Railway deployment should work now")
        print("🚀 Push your changes to GitHub to deploy")
    else:
        print("\n❌ Tests failed!")
        print("🔧 Check the error messages above")

if __name__ == '__main__':
    main()
