@echo off
chcp 65001 >nul
title Paper Translator

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [错误] 未找到虚拟环境，请先运行 install_windows.bat
    pause
    exit /b 1
)

REM Run the application
python main.py

REM Keep console open on exit
pause