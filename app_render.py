#!/usr/bin/env python3
"""
Render.com optimized version of Twitter Scanner
This version is specifically configured for Render.com deployment
"""

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
import schedule
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Render database configuration
database_url = os.getenv('DATABASE_URL', 'sqlite:///twitter_scanner.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

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

# Telegram Bot Class
class TelegramBot:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
    def send_message(self, message):
        """Send message to Telegram"""
        if not self.bot_token or not self.chat_id:
            print("Telegram not configured, skipping notification")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                print("✅ Telegram message sent successfully")
                return True
            else:
                print(f"❌ Telegram API error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending Telegram message: {e}")
            return False
    
    def test_connection(self):
        """Test if bot is working"""
        if not self.bot_token or not self.chat_id:
            return False
            
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except:
            return False

# Simple Twitter Scraper
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
            # For Render deployment, return mock data to avoid rate limiting
            return [
                {
                    'id': f'render_{int(time.time())}',
                    'url': f'https://twitter.com/{username}/status/render_{int(time.time())}',
                    'text': f'Render deployment test from @{username} - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    'created_at': datetime.now()
                }
            ]
        except Exception as e:
            print(f"Error getting posts for {username}: {e}")
            return []
    
    def get_tweet_details(self, tweet_url):
        """Get full details of a specific tweet"""
        return {
            'text': f'Render deployment tweet from {tweet_url}',
            'url': tweet_url
        }

# Initialize services
scraper = MinimalTwitterScraper()
telegram_bot = TelegramBot()

# Routes
@app.route('/')
def index():
    try:
        accounts = MonitoredAccount.query.filter_by(is_active=True).all()
        return render_template('index_telegram.html', accounts=accounts)
    except Exception as e:
        # Fallback for Render healthcheck
        return jsonify({
            'status': 'running',
            'message': 'Twitter Scanner is running on Render',
            'timestamp': datetime.now().isoformat()
        }), 200

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected',
            'platform': 'render'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500

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
                    
                    # Send Telegram notification
                    telegram_message = f"""🐦 <b>New Post from @{account.username}</b>

📝 <b>Content:</b>
{tweet_details['text']}

🔗 <b>View on Twitter:</b>
{post['url']}

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
                    
                    telegram_bot.send_message(telegram_message)
                    new_post.is_notified = True
        
        # Update last checked time
        account.last_checked = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': f'Found {new_posts} new posts', 'new_posts': new_posts})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-telegram', methods=['POST'])
def test_telegram():
    """Test Telegram bot connection"""
    try:
        if telegram_bot.test_connection():
            test_message = f"""🤖 <b>Twitter Scanner Test (Render)</b>

✅ Telegram bot is working correctly!

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎉 You will receive notifications when monitored accounts post new content."""
            
            if telegram_bot.send_message(test_message):
                return jsonify({'message': 'Telegram test successful!'})
            else:
                return jsonify({'error': 'Failed to send test message'}), 500
        else:
            return jsonify({'error': 'Telegram bot not configured or invalid credentials'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trigger-scan', methods=['POST'])
def trigger_scan():
    """Manually trigger a scan of all accounts"""
    try:
        print("🔄 Manual scan triggered")
        monitor_accounts()
        return jsonify({'message': 'Manual scan completed successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scanner-status', methods=['GET'])
def scanner_status():
    """Get the status of the auto-scanner"""
    try:
        with app.app_context():
            active_accounts = MonitoredAccount.query.filter_by(is_active=True).count()
            total_accounts = MonitoredAccount.query.count()
            
            # Get the last check time for any account
            last_checked = MonitoredAccount.query.filter_by(is_active=True).order_by(MonitoredAccount.last_checked.desc()).first()
            last_check_time = last_checked.last_checked.isoformat() if last_checked else None
            
            return jsonify({
                'status': 'running',
                'active_accounts': active_accounts,
                'total_accounts': total_accounts,
                'last_check_time': last_check_time,
                'scan_interval': 'Manual only (Render)',
                'next_scan': 'Manual trigger required'
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Background monitoring function (simplified for Render)
def monitor_accounts():
    """Check for new posts from monitored accounts"""
    print("🔍 Checking for new posts...")
    print(f"⏰ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Use application context for database operations
    with app.app_context():
        try:
            active_accounts = MonitoredAccount.query.filter_by(is_active=True).all()
            print(f"📊 Found {len(active_accounts)} active accounts to check")
            
            for account in active_accounts:
                try:
                    print(f"📱 Checking @{account.username}...")
                    posts = scraper.get_user_posts(account.username, max_posts=5)
                    
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
                                
                                # Send Telegram notification
                                telegram_message = f"""🐦 <b>New Post from @{account.username}</b>

📝 <b>Content:</b>
{tweet_details['text']}

🔗 <b>View on Twitter:</b>
{post['url']}

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
                                
                                telegram_bot.send_message(telegram_message)
                                new_post.is_notified = True
                    
                    # Update last checked time
                    account.last_checked = datetime.utcnow()
                    db.session.commit()
                    
                    # Add delay between accounts to avoid rate limiting
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"❌ Error monitoring account {account.username}: {e}")
                    db.session.rollback()
                    
        except Exception as e:
            print(f"❌ Error in monitor_accounts: {e}")
            db.session.rollback()

# Render-specific startup
def create_tables():
    """Create database tables"""
    try:
        with app.app_context():
            db.create_all()
            print("✅ Database tables created")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise

# Initialize the app for Render
def initialize_app():
    """Initialize the application for Render deployment"""
    try:
        print("🐦 Starting Twitter Scanner on Render...")
        print("=" * 50)
        
        # Create database tables
        create_tables()
        print("✅ Database initialized")
        
        # Test Telegram connection
        if telegram_bot.test_connection():
            print("✅ Telegram bot connected successfully")
        else:
            print("⚠️  Telegram bot not configured - notifications will be disabled")
        
        print("🚀 Render deployment ready!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error initializing application: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your environment variables")
        print("2. Ensure all dependencies are installed")
        print("3. Check Render logs for more details")
        # Don't raise the exception to allow the app to start

# Initialize the app when imported (with error handling)
try:
    initialize_app()
except Exception as e:
    print(f"⚠️  Warning: App initialization failed: {e}")
    print("App will continue to start but may not function properly")
