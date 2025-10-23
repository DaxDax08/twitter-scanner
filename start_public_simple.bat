@echo off
echo ========================================
echo  Twitter Scanner - Public Access
echo ========================================
echo.

echo Starting Twitter Scanner...
python app_telegram.py

echo.
echo ========================================
echo  To make it public, choose an option:
echo ========================================
echo.
echo Option 1 - ngrok (Recommended):
echo   1. Download from: https://ngrok.com/download
echo   2. Extract ngrok.exe to this folder
echo   3. Run: ngrok http 5000
echo   4. Copy the public URL (like https://abc123.ngrok.io)
echo.
echo Option 2 - Serveo (No installation):
echo   Run: ssh -R 80:localhost:5000 serveo.net
echo.
echo Option 3 - localhost.run:
echo   Run: ssh -R 80:localhost:5000 localhost.run
echo.
echo Option 4 - Cloudflare Tunnel:
echo   Run: cloudflared tunnel --url http://localhost:5000
echo.
pause
