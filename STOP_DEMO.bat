@echo off
title SecureShare Platform Shutdown
echo =====================================================================
echo                Stopping SecureShare Platform Services
echo =====================================================================
echo.

echo [*] Terminating Backend process (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a 2>nul
)

echo [*] Terminating Frontend process (Port 5173)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173 ^| findstr LISTENING') do (
    taskkill /F /PID %%a 2>nul
)

taskkill /FI "WINDOWTITLE eq SecureShare-Backend*" /T /F 2>nul
taskkill /FI "WINDOWTITLE eq SecureShare-Frontend*" /T /F 2>nul

echo [+] All SecureShare demo servers successfully stopped.
echo.
pause
