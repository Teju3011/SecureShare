@echo off
title SECURESHARE Platform Launcher
echo ===================================================
echo Starting SECURESHARE Platform (Backend + Frontend)
echo ===================================================

cd /d "%~dp0backend"
echo [*] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "SecureShare-Backend" cmd /k ".\venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3 /nobreak >nul

cd /d "%~dp0frontend"
echo [*] Starting Vite Frontend on http://localhost:5173 ...
start "SecureShare-Frontend" cmd /k "npm run dev"

echo.
echo ===================================================
echo [!] Both servers started in separate terminal windows.
echo [!] Open Web Browser at: http://localhost:5173
echo [!] Interactive Swagger Docs: http://127.0.0.1:8000/docs
echo ===================================================
pause
