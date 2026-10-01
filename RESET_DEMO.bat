@echo off
title SecureShare Database & Storage Reset
echo =====================================================================
echo                Resetting SecureShare Demo Environment
echo =====================================================================
echo.

cd /d "%~dp0"

echo [*] Stopping running instances first...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a 2>nul
)

echo [*] Resetting SQLite database and seeding pristine persona records...
if exist secureshare.db del secureshare.db
if exist backend\secureshare.db del backend\secureshare.db

call backend\venv\Scripts\python.exe backend\app\seed.py

echo.
echo [+] Demo environment successfully reset to fresh, verified state!
echo [+] You can now run START_DEMO.bat to begin a fresh review session.
echo.
pause
