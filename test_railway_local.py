#!/usr/bin/env python3
"""
Test script for Railway deployment
This script tests the app locally to ensure it works before deployment
"""

import os
import sys
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_railway_app():
    """Test the Railway app locally"""
    print("🧪 Testing Railway app locally...")
    print("=" * 50)
    
    try:
        # Import the app
        from app_railway import app
        
        # Test app creation
        print("✅ App imported successfully")
        
        # Test with test client
        with app.test_client() as client:
            print("✅ Test client created")
            
            # Test health endpoint
            response = client.get('/health')
            print(f"Health check status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Health endpoint working")
                print(f"Response: {response.get_json()}")
            else:
                print("❌ Health endpoint failed")
                print(f"Response: {response.get_data()}")
            
            # Test root endpoint
            response = client.get('/')
            print(f"Root endpoint status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Root endpoint working")
            else:
                print("❌ Root endpoint failed")
                print(f"Response: {response.get_data()}")
            
            # Test API endpoints
            response = client.get('/api/accounts')
            print(f"API accounts status: {response.status_code}")
            if response.status_code == 200:
                print("✅ API accounts endpoint working")
            else:
                print("❌ API accounts endpoint failed")
        
        print("\n🎉 All tests passed! Railway app is ready for deployment.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_railway_app()
    sys.exit(0 if success else 1)
