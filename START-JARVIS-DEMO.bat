@echo off
setlocal
title J-A-R-V-I-S Demo Launcher
cd /d "%~dp0"
echo J-A-R-V-I-S DEMO
where py >nul 2>nul || (echo Install Python 3.12+ & pause & exit /b 1)
where node >nul 2>nul || (echo Install Node.js 20+ & pause & exit /b 1)
if not exist "backend\.venv" py -3.12 -m venv backend\.venv
if errorlevel 1 (echo Python 3.12 setup failed & pause & exit /b 1)
backend\.venv\Scripts\python.exe -m pip install -e backend
if errorlevel 1 (echo Backend install failed & pause & exit /b 1)
if not exist "frontend\node_modules" (cd frontend & npm install & cd ..)
if errorlevel 1 (echo Frontend install failed & pause & exit /b 1)
start "J-A-R-V-I-S Backend" cmd /k "cd /d "%~dp0backend" && .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
start "J-A-R-V-I-S Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev -- --host 127.0.0.1"
timeout /t 5 /nobreak >nul
start "" "http://127.0.0.1:5173"
echo Demo launched. Keep both terminal windows open.
echo Configure backend\.env to enable real AI responses.
pause
