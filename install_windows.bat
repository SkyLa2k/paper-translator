@echo off
chcp 65001 >nul
title Paper Translator Setup

echo ======================================
echo   Paper Translator 安装脚本
echo ======================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.10+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] 正在创建虚拟环境...
python -m venv venv
if errorlevel 1 (
    echo [错误] 虚拟环境创建失败
    pause
    exit /b 1
)

echo [2/4] 正在安装依赖...
call venv\Scripts\pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo [3/4] 正在创建配置文件...
if not exist "config\config.yaml" (
    copy config\config.yaml.example config\config.yaml
    echo [提示] 请编辑 config\config.yaml 填入你的 API Key
)

echo [4/4] 安装完成!
echo.
echo ====================
echo   下一步操作:
echo ====================
echo 1. 编辑 config\config.yaml，填入你的 Gemini API Key
echo 2. 运行 run.bat 启动程序
echo.
echo API Key 申请: https://aistudio.google.com/app/apikey
echo.
pause