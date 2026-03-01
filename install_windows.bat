@echo off
chcp 65001 >nul
title Paper Translator Setup

echo ======================================
echo   Paper Translator - Setup
echo ======================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/4] Installing dependencies...
call venv\Scripts\pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [3/4] Creating config file...
if not exist "config\config.yaml" (
    copy config\config.yaml.example config\config.yaml
    echo [INFO] Please edit config\config.yaml to add your API Key
)

echo [4/4] Setup complete!
echo.
echo ====================
echo   Next steps:
echo ====================
echo 1. Edit config\config.yaml and add your Gemini API Key
echo 2. Run run_windows.bat to start
echo.
echo Get API Key: https://aistudio.google.com/app/apikey
echo.
pause