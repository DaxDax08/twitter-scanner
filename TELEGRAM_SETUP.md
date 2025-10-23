# Telegram Setup Guide for Twitter Scanner

## 🤖 Step 1: Create a Telegram Bot

1. **Open Telegram** on your phone or computer
2. **Search for @BotFather** in Telegram
3. **Start a chat** with BotFather
4. **Send the command:** `/newbot`
5. **Choose a name** for your bot (e.g., "My Twitter Scanner")
6. **Choose a username** for your bot (must end with 'bot', e.g., "my_twitter_scanner_bot")
7. **Copy the bot token** that BotFather gives you (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## 💬 Step 2: Get Your Chat ID

### Method 1: Using @userinfobot
1. **Search for @userinfobot** in Telegram
2. **Start a chat** with @userinfobot
3. **Send any message** to @userinfobot
4. **Copy your Chat ID** (looks like: `123456789`)

### Method 2: Using your bot
1. **Start a chat** with your new bot
2. **Send any message** to your bot (like "Hello")
3. **Go to:** `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. **Find your Chat ID** in the response (look for "chat":{"id":123456789})

## ⚙️ Step 3: Configure the Scanner

1. **Create a `.env` file** in your scanner folder with:
```env
SECRET_KEY=your-secret-key-here
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

2. **Replace the values:**
   - `your_bot_token_here` → Your bot token from BotFather
   - `your_chat_id_here` → Your chat ID from step 2

## 🚀 Step 4: Run the Scanner

1. **Stop the current scanner** (Ctrl+C in Command Prompt)
2. **Run the Telegram version:**
   ```cmd
   python app_telegram.py
   ```

3. **Test the connection:**
   - Open your browser to `http://localhost:5000`
   - Look for a "Test Telegram" button
   - Click it to send a test message

## 📱 Step 5: Test Notifications

1. **Add a Twitter account** to monitor
2. **Click "Check Now"** to trigger a manual check
3. **You should receive a Telegram message** with the post details

## 🔧 Troubleshooting

### "Telegram bot not configured"
- Check your `.env` file has the correct token and chat ID
- Make sure there are no extra spaces in the values

### "Failed to send test message"
- Verify your bot token is correct
- Make sure you've started a chat with your bot
- Check that your chat ID is correct

### "Telegram API error"
- Your bot token might be invalid
- Try creating a new bot with BotFather

## 📋 Example .env File

```env
SECRET_KEY=my-secret-key-123
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

## 🎉 You're Done!

Once configured, you'll receive beautiful Telegram messages like:

```
🐦 New Post from @username

📝 Content:
This is the tweet content...

🔗 View on Twitter:
https://twitter.com/username/status/123456

⏰ Time: 2024-01-15 14:30:25
```

The scanner will automatically check for new posts every 5 minutes and send you notifications!

