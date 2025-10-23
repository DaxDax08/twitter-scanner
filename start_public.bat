@echo off
echo ========================================
echo  Twitter Scanner - Public Access
echo ========================================
echo.

echo Starting Twitter Scanner...
start "Twitter Scanner" python app_telegram.py

echo Waiting for app to start...
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo  Choose your tunneling method:
echo ========================================
echo 1. ngrok (Recommended - most reliable)
echo 2. localtunnel (Simple alternative)
echo 3. Manual setup instructions
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" goto ngrok
if "%choice%"=="2" goto localtunnel
if "%choice%"=="3" goto manual
goto end

:ngrok
echo.
echo Starting ngrok tunnel...
echo After ngrok starts, you'll see a public URL like: https://abc123.ngrok.io
echo Share this URL to access your dashboard from anywhere!
echo.
ngrok http 5000
goto end

:localtunnel
echo.
echo Installing and starting localtunnel...
npm install -g localtunnel
lt --port 5000 --subdomain twitter-scanner-%RANDOM%
goto end

:manual
echo.
echo ========================================
echo  Manual Setup Instructions:
echo ========================================
echo 1. Download ngrok from: https://ngrok.com/download
echo 2. Extract ngrok.exe to this folder
echo 3. Run: ngrok http 5000
echo 4. Copy the public URL (like https://abc123.ngrok.io)
echo 5. Share this URL to access from anywhere!
echo.
echo Alternative services:
echo - Cloudflare Tunnel (free, more secure)
echo - Serveo (no installation needed)
echo - localhost.run (simple SSH tunnel)
echo.
pause
goto end

:end
echo.
echo Press any key to stop the application...
pause >nul
taskkill /f /im python.exe >nul 2>&1
