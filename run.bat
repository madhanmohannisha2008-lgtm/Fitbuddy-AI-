@echo off
cd /d "%~dp0"
title FitBuddy - AI Fitness Plan Generator
echo ========================================================
echo   FitBuddy - AI Fitness Plan Generator Launcher
echo ========================================================
echo.

:: 1. Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 goto :NoPython

:: 2. Create virtual environment if it doesn't exist
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 goto :VenvError
) else (
    echo [INFO] Virtual environment detected.
)

:: 3. Activate the virtual environment
echo [INFO] Activating virtual environment...
call "venv\Scripts\activate.bat"
if errorlevel 1 goto :ActivateError
echo [INFO] Virtual environment activated: %VIRTUAL_ENV%

:: 4. Install or update dependencies
echo [INFO] Installing dependencies from requirements.txt...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 goto :PipError

:: 5. Check for .env file
if not exist ".env" (
    echo [WARNING] .env file not found! Creating template .env file...
    echo GOOGLE_API_KEY=your_gemini_api_key_here> .env
    echo GEMINI_MODEL=gemini-3.8-flash>> .env
    echo MAX_OUTPUT_TOKENS=550>> .env
    echo TIP_MAX_TOKENS=80>> .env
    echo.
    echo [ACTION REQUIRED] Open the .env file, paste your actual Google Gemini API key,
    echo save it, and run this script again.
    pause
    exit /b 1
)

:: 6. Launch FastAPI application with Uvicorn
echo.
echo ========================================================
echo   Starting FitBuddy Server...
echo   Web UI:        http://127.0.0.1:8000
echo   Admin Panel:   http://127.0.0.1:8000/view-all-users
echo   Swagger Docs:  http://127.0.0.1:8000/docs
echo ========================================================
echo.

start http://127.0.0.1:8000
uvicorn app.main:app --reload
goto :eof

:NoPython
echo [ERROR] Python is not installed or not added to PATH.
pause
exit /b 1

:VenvError
echo [ERROR] Failed to create virtual environment.
pause
exit /b 1

:ActivateError
echo [ERROR] Failed to activate virtual environment.
pause
exit /b 1

:PipError
echo [ERROR] Failed to install dependencies from requirements.txt.
pause
exit /b 1