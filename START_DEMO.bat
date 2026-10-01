@echo off
title SecureShare Live Demonstration Launcher
echo =====================================================================
echo           SECURESHARE — ENTERPRISE FILE SECURITY PLATFORM
echo     Continuous Threat Validation ^& IEEE 29148 Compliance Capstone
echo =====================================================================
echo.

cd /d "%~dp0"

echo [*] Initializing database and verifying demo personas...
call backend\venv\Scripts\python.exe backend\app\seed.py

echo.
echo [*] Launching FastAPI Backend on http://127.0.0.1:8000 ...
start "SecureShare-Backend" cmd /k "cd /d ""%~dp0backend"" && .\venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo [*] Launching React Vite Frontend on http://localhost:5173 ...
start "SecureShare-Frontend" cmd /k "cd /d ""%~dp0frontend"" && npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo =====================================================================
echo  DEMO PERSONA CREDENTIALS (All passwords: Pass123!Secure)
echo =====================================================================
echo  - Sushmitha Reddy (Product Owner):   sushmitha@example.com
echo  - Rahul Kumar (Crypto Engineer):     rahul@example.com
echo  - Priya Sharma (DevSecOps Lead):     priya@example.com
echo  - Arjun Rao (UI/UX Engineer):        arjun@example.com
echo  - System Administrator (SOC Admin):  admin@example.com
echo  - Security Auditor (Compliance):     auditor@example.com
echo =====================================================================
echo.
echo [*] Opening presentation demo dashboard in browser...
start http://localhost:5173/demo

echo [!] Demo environment is live. Press any key to exit this launcher window.
pause >nul
