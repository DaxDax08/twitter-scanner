# 🐦 Twitter Scanner

A powerful Twitter monitoring dashboard that tracks accounts and notifies you of new posts via Telegram.

## ✨ Features

- 🔍 **Monitor Multiple Accounts**: Track unlimited Twitter accounts
- 🔔 **Real-time Notifications**: Get instant Telegram alerts for new posts
- 📱 **Mobile-Friendly**: Access from any device, anywhere
- 🔍 **Search & Filter**: Find accounts quickly with built-in search
- 📊 **Status Dashboard**: Monitor scanner status and statistics
- 🌐 **Public Access**: Access from anywhere via public URL

## 🚀 Quick Start

### Option 1: Local Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/twitter-scanner.git
cd twitter-scanner

# Install dependencies
pip install -r requirements.txt

# Run the application
python app_telegram.py
```

### Option 2: Deploy to Cloud (Recommended)
Choose from these free hosting options:

#### Railway.app
1. Fork this repository
2. Go to [Railway.app](https://railway.app)
3. Connect your GitHub account
4. Deploy from GitHub repository
5. Get your public URL!

#### Render.com
1. Fork this repository
2. Go to [Render.com](https://render.com)
3. Create new Web Service
4. Connect your GitHub repository
5. Deploy and get your public URL!

#### Vercel (Serverless)
1. Fork this repository
2. Go to [Vercel.com](https://vercel.com)
3. Import your GitHub repository
4. Deploy and get your public URL!

## 🔧 Configuration

### Environment Variables
Set these in your hosting platform:

```bash
SECRET_KEY=your-secret-key-here
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id
```

### Telegram Setup
1. Create a bot with [@BotFather](https://t.me/botfather)
2. Get your bot token
3. Start a chat with your bot
4. Get your chat ID
5. Add these to your environment variables

## 📱 Usage

1. **Add Accounts**: Click "Add Account" to monitor Twitter users
2. **Search**: Use the search bar to find specific accounts
3. **Filter**: Filter by active/inactive status
4. **Check Status**: View scanner statistics and status
5. **Manual Scan**: Trigger immediate scans of all accounts

## 🌐 Public Access

Once deployed, your dashboard will be accessible from:
- ✅ Any computer
- ✅ Any phone or tablet
- ✅ From anywhere in the world
- ✅ No network restrictions

## 🛠️ Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run in development mode
python app_telegram.py
```

### Adding Features
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📊 API Endpoints

- `GET /` - Main dashboard
- `GET /api/accounts` - List all accounts
- `POST /api/accounts` - Add new account
- `DELETE /api/accounts/<id>` - Remove account
- `POST /api/accounts/<id>/toggle` - Toggle account status
- `GET /api/posts/<id>` - Get account posts
- `POST /api/check/<id>` - Manual check
- `GET /api/scanner-status` - Scanner status
- `POST /api/trigger-scan` - Trigger manual scan

## 🔒 Security

For production use, consider:
- Adding authentication
- Using environment variables for secrets
- Setting up proper database backups
- Implementing rate limiting

## 📄 License

MIT License - feel free to use and modify!

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

If you have any questions or issues:
1. Check the [Issues](https://github.com/yourusername/twitter-scanner/issues) page
2. Create a new issue with detailed information
3. Join our community discussions

---

**Made with ❤️ for the Twitter community**