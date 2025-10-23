#!/usr/bin/env python3
"""
Generate a secure SECRET_KEY for Railway deployment
"""

import secrets
import string

def generate_secret_key():
    """Generate a secure secret key for Flask"""
    # Generate a 32-character random string
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(32))
    return secret_key

def main():
    print("🔐 Generating SECRET_KEY for Railway")
    print("=" * 50)
    
    # Generate the secret key
    secret_key = generate_secret_key()
    
    print("✅ Generated secure SECRET_KEY:")
    print(f"SECRET_KEY={secret_key}")
    print()
    print("📋 Copy this value and update it in Railway:")
    print("1. Go to your Railway dashboard")
    print("2. Click on your twitter-scanner service")
    print("3. Go to Variables tab")
    print("4. Click on SECRET_KEY")
    print("5. Replace 'your-secret-key-here' with the key above")
    print("6. Save the changes")
    print()
    print("🔒 This is a secure, randomly generated key")
    print("💡 Keep this key safe - don't share it publicly")

if __name__ == '__main__':
    main()

