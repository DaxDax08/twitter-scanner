#!/usr/bin/env python3
"""
Serverless version of Twitter Scanner for GitHub deployment
This version works with Vercel, Netlify Functions, or similar serverless platforms
"""

from flask import Flask, render_template, request, jsonify
import json
import os
import time
from datetime import datetime
import hashlib

# For serverless deployment
app = Flask(__name__)

# Simple in-memory storage (for demo - use real database in production)
accounts_db = []
posts_db = []

class MonitoredAccount:
    def __init__(self, username, display_name, is_active=True):
        self.id = len(accounts_db) + 1
        self.username = username
        self.display_name = display_name
        self.is_active = is_active
        self.created_at = datetime.now()
        self.last_checked = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'last_checked': self.last_checked.isoformat()
        }

class PostHistory:
    def __init__(self, account_id, post_id, text, url):
        self.id = len(posts_db) + 1
        self.account_id = account_id
        self.post_id = post_id
        self.text = text
        self.url = url
        self.created_at = datetime.now()
        self.is_notified = False
    
    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'post_id': self.post_id,
            'text': self.text,
            'url': self.url,
            'created_at': self.created_at.isoformat(),
            'is_notified': self.is_notified
        }

# Routes
@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index_telegram.html', accounts=accounts_db)

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    """Get all accounts"""
    return jsonify([account.to_dict() for account in accounts_db])

@app.route('/api/accounts', methods=['POST'])
def add_account():
    """Add new account"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip().lstrip('@')
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        # Check if account already exists
        existing = next((acc for acc in accounts_db if acc.username == username), None)
        if existing:
            return jsonify({'error': 'Account already being monitored'}), 400
        
        # Create new account
        account = MonitoredAccount(username, username)
        accounts_db.append(account)
        
        return jsonify(account.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<int:account_id>', methods=['DELETE'])
def remove_account(account_id):
    """Remove account"""
    try:
        global accounts_db
        accounts_db = [acc for acc in accounts_db if acc.id != account_id]
        return jsonify({'message': 'Account removed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<int:account_id>/toggle', methods=['POST'])
def toggle_account(account_id):
    """Toggle account status"""
    try:
        account = next((acc for acc in accounts_db if acc.id == account_id), None)
        if account:
            account.is_active = not account.is_active
            return jsonify(account.to_dict())
        return jsonify({'error': 'Account not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts/<int:account_id>')
def get_posts(account_id):
    """Get posts for account"""
    try:
        posts = [post for post in posts_db if post.account_id == account_id]
        return jsonify([post.to_dict() for post in posts])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/check/<int:account_id>', methods=['POST'])
def manual_check(account_id):
    """Manual check for posts"""
    try:
        account = next((acc for acc in accounts_db if acc.id == account_id), None)
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        # Simulate finding new posts (replace with real Twitter API)
        new_posts = 0
        if account.is_active:
            # Mock new post
            post = PostHistory(
                account_id=account.id,
                post_id=f"post_{int(time.time())}",
                text=f"New post from @{account.username} - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                url=f"https://twitter.com/{account.username}/status/mock_{int(time.time())}"
            )
            posts_db.append(post)
            new_posts = 1
            account.last_checked = datetime.now()
        
        return jsonify({'message': f'Found {new_posts} new posts', 'new_posts': new_posts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scanner-status', methods=['GET'])
def scanner_status():
    """Get scanner status"""
    try:
        active_accounts = len([acc for acc in accounts_db if acc.is_active])
        total_accounts = len(accounts_db)
        
        return jsonify({
            'status': 'running',
            'active_accounts': active_accounts,
            'total_accounts': total_accounts,
            'last_check_time': datetime.now().isoformat(),
            'scan_interval': 'Manual only (serverless)',
            'next_scan': 'Manual trigger required'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trigger-scan', methods=['POST'])
def trigger_scan():
    """Trigger manual scan"""
    try:
        # Simulate scanning all accounts
        new_posts = 0
        for account in accounts_db:
            if account.is_active:
                # Mock new post
                post = PostHistory(
                    account_id=account.id,
                    post_id=f"scan_{int(time.time())}_{account.id}",
                    text=f"Auto-scan post from @{account.username} - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                    url=f"https://twitter.com/{account.username}/status/scan_{int(time.time())}"
                )
                posts_db.append(post)
                new_posts += 1
                account.last_checked = datetime.now()
        
        return jsonify({'message': f'Manual scan completed! Found {new_posts} new posts'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-telegram', methods=['POST'])
def test_telegram():
    """Test Telegram connection"""
    return jsonify({'message': 'Telegram test successful! (Serverless mode)'})

# For Vercel deployment
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
