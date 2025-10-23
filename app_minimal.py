from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
import time
import threading
from datetime import datetime
import json
import re
import os
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitter_scanner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)
CORS(app)

# Database Models
class MonitoredAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    profile_image_url = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name,
            'profile_image_url': self.profile_image_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'last_checked': self.last_checked.isoformat()
        }

class PostHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('monitored_account.id'), nullable=False)
    post_id = db.Column(db.String(100), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(200))
    is_notified = db.Column(db.Boolean, default=False)
    post_hash = db.Column(db.String(64), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'post_id': self.post_id,
            'text': self.text,
            'created_at': self.created_at.isoformat(),
            'url': self.url,
            'is_notified': self.is_notified
        }

# Simple Twitter Scraper (minimal dependencies)
class MinimalTwitterScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_user_profile(self, username):
        """Get user profile information"""
        try:
            url = f"https://twitter.com/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                return {
                    'username': username,
                    'display_name': username,
                    'profile_image_url': '',
                    'exists': True
                }
            else:
                return {'exists': False}
                
        except Exception as e:
            print(f"Error getting profile for {username}: {e}")
            return {'exists': False}
    
    def get_user_posts(self, username, max_posts=5):
        """Get recent posts from a user's profile"""
        try:
            # For now, return mock data to test the interface
            return [
                {
                    'id': f'mock_{int(time.time())}',
                    'url': f'https://twitter.com/{username}/status/mock_{int(time.time())}',
                    'text': f'Mock post from @{username} - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    'created_at': datetime.now()
                }
            ]
        except Exception as e:
            print(f"Error getting posts for {username}: {e}")
            return []
    
    def get_tweet_details(self, tweet_url):
        """Get full details of a specific tweet"""
        return {
            'text': f'Mock tweet content from {tweet_url}',
            'url': tweet_url
        }

# Initialize services
scraper = MinimalTwitterScraper()

# Routes
@app.route('/')
def index():
    try:
        accounts = MonitoredAccount.query.filter_by(is_active=True).all()
        return render_template('index.html', accounts=accounts)
    except Exception as e:
        return f"Error loading page: {str(e)}", 500

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    try:
        accounts = MonitoredAccount.query.all()
        return jsonify([account.to_dict() for account in accounts])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts', methods=['POST'])
def add_account():
    try:
        data = request.get_json()
        username = data.get('username', '').strip().lstrip('@')
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        # Check if account already exists
        existing = MonitoredAccount.query.filter_by(username=username).first()
        if existing:
            return jsonify({'error': 'Account already being monitored'}), 400
        
        # Get user info from Twitter
        user_info = scraper.get_user_profile(username)
        if not user_info.get('exists'):
            return jsonify({'error': 'User not found on Twitter'}), 400
        
        # Create new monitored account
        account = MonitoredAccount(
            username=username,
            display_name=user_info.get('display_name', username),
            profile_image_url=user_info.get('profile_image_url', '')
        )
        
        db.session.add(account)
        db.session.commit()
        
        return jsonify(account.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<int:account_id>', methods=['DELETE'])
def remove_account(account_id):
    try:
        account = MonitoredAccount.query.get_or_404(account_id)
        db.session.delete(account)
        db.session.commit()
        return jsonify({'message': 'Account removed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<int:account_id>/toggle', methods=['POST'])
def toggle_account(account_id):
    try:
        account = MonitoredAccount.query.get_or_404(account_id)
        account.is_active = not account.is_active
        db.session.commit()
        return jsonify(account.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts/<int:account_id>')
def get_posts(account_id):
    try:
        posts = PostHistory.query.filter_by(account_id=account_id).order_by(PostHistory.created_at.desc()).limit(20).all()
        return jsonify([post.to_dict() for post in posts])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/check/<int:account_id>', methods=['POST'])
def manual_check(account_id):
    """Manually check for new posts from a specific account"""
    try:
        account = MonitoredAccount.query.get_or_404(account_id)
        
        posts = scraper.get_user_posts(account.username, max_posts=5)
        new_posts = 0
        
        for post in posts:
            # Check if we already have this post
            existing = PostHistory.query.filter_by(post_id=post['id']).first()
            if not existing:
                # Get full tweet details
                tweet_details = scraper.get_tweet_details(post['url'])
                
                # Create post hash for duplicate detection
                post_hash = hashlib.md5(tweet_details['text'].encode()).hexdigest()
                
                # Check for duplicate content
                duplicate = PostHistory.query.filter_by(post_hash=post_hash).first()
                if not duplicate:
                    # Create new post record
                    new_post = PostHistory(
                        account_id=account.id,
                        post_id=post['id'],
                        text=tweet_details['text'],
                        created_at=post['created_at'],
                        url=post['url'],
                        post_hash=post_hash
                    )
                    db.session.add(new_post)
                    new_posts += 1
        
        # Update last checked time
        account.last_checked = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': f'Found {new_posts} new posts', 'new_posts': new_posts})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        print("🐦 Starting Twitter Scanner...")
        print("=" * 50)
        
        # Create database tables
        with app.app_context():
            db.create_all()
            print("✅ Database initialized")
        
        print("🚀 Starting web server...")
        print("📱 Open your browser to: http://localhost:5000")
        print("=" * 50)
        
        # Start the Flask app
        app.run(debug=True, host='127.0.0.1', port=5000)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure Python is installed")
        print("2. Run: pip install flask flask-sqlalchemy flask-cors requests")
        print("3. Check if port 5000 is available")
        input("Press Enter to exit...")

