@echo off
chcp 65001 >nul
title Paper Translator

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] Virtual environment not found. Please run install_windows.bat first.
    pause
    exit /b 1
)

REM Run the application
python main.py

REM Keep console open on exit
pause