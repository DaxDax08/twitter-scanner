#!/usr/bin/env python3
"""
Test script for Twitter scraper functionality
Run this to test if the scraper can fetch data from Twitter
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import TwitterScraper

def test_scraper():
    """Test the Twitter scraper with a public account"""
    print("🧪 Testing Twitter Scraper...")
    print("=" * 50)
    
    scraper = TwitterScraper()
    
    # Test with a well-known public account
    test_username = "elonmusk"  # Elon Musk's account (usually public and active)
    
    print(f"📱 Testing with @{test_username}...")
    
    try:
        # Test profile fetching
        print("1. Testing profile fetch...")
        profile = scraper.get_user_profile(test_username)
        
        if profile.get('exists'):
            print(f"   ✅ Profile found: {profile.get('display_name', 'Unknown')}")
        else:
            print("   ❌ Profile not found")
            return False
        
        # Test posts fetching
        print("2. Testing posts fetch...")
        posts = scraper.get_user_posts(test_username, max_posts=3)
        
        if posts:
            print(f"   ✅ Found {len(posts)} posts")
            for i, post in enumerate(posts[:2], 1):
                print(f"   Post {i}: {post['text'][:50]}...")
        else:
            print("   ⚠️  No posts found (this might be normal)")
        
        # Test individual tweet details
        if posts:
            print("3. Testing tweet details...")
            first_post = posts[0]
            details = scraper.get_tweet_details(first_post['url'])
            if details['text']:
                print(f"   ✅ Tweet details: {details['text'][:50]}...")
            else:
                print("   ⚠️  Could not fetch tweet details")
        
        print("\n🎉 Scraper test completed successfully!")
        print("   The scraper should work for monitoring accounts.")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("   - Check your internet connection")
        print("   - Twitter might be blocking requests")
        print("   - Try running the test again")
        return False

def main():
    """Main test function"""
    print("Twitter Scanner - Scraper Test")
    print("This will test if the scraper can fetch data from Twitter")
    print()
    
    success = test_scraper()
    
    if success:
        print("\n✅ All tests passed! You can now run the main application.")
        print("   Run: python app.py")
    else:
        print("\n❌ Tests failed. Please check the error messages above.")
        print("   The scraper might need adjustments for your environment.")

if __name__ == '__main__':
    main()

