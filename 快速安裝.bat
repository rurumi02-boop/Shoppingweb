@echo off
chcp 65001 >nul
title 安裝 Python 依賴套件
color 0B

echo.
echo ========================================
echo   安裝 CampingData 專案依賴套件
echo ========================================
echo.

REM 檢查是否在正確的目錄
if not exist "requirements.txt" (
    echo [錯誤] 請在專案根目錄執行此腳本
    echo 當前目錄：%CD%
    pause
    exit /b 1
)

echo 正在檢查 Python 安裝...
echo.

REM 嘗試多種方式執行 pip
set INSTALLED=0

REM 方法 1：直接使用 pip
pip --version >nul 2>&1
if not errorlevel 1 (
    echo [✓] 找到 pip 命令
    echo.
    echo 正在安裝依賴套件...
    pip install -r requirements.txt
    if not errorlevel 1 (
        set INSTALLED=1
    )
)

REM 方法 2：使用 python -m pip
if %INSTALLED%==0 (
    python -m pip --version >nul 2>&1
    if not errorlevel 1 (
        echo [✓] 找到 python -m pip
        echo.
        echo 正在安裝依賴套件...
        python -m pip install -r requirements.txt
        if not errorlevel 1 (
            set INSTALLED=1
        )
    )
)

REM 方法 3：使用 py 啟動器
if %INSTALLED%==0 (
    py -m pip --version >nul 2>&1
    if not errorlevel 1 (
        echo [✓] 找到 py -m pip
        echo.
        echo 正在安裝依賴套件...
        py -m pip install -r requirements.txt
        if not errorlevel 1 (
            set INSTALLED=1
        )
    )
)

if %INSTALLED%==0 (
    echo.
    echo ========================================
    echo [❌] 無法找到 pip
    echo ========================================
    echo.
    echo 可能的原因：
    echo 1. Python 未安裝
    echo 2. Python 未加入 PATH 環境變數
    echo.
    echo 解決方法：
    echo 1. 安裝 Python：https://www.python.org/downloads/
    echo 2. 安裝時務必勾選 "Add Python to PATH"
    echo 3. 重新啟動命令提示字元
    echo 4. 查看「安裝Python和pip指南.md」了解詳細步驟
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [✅] 安裝完成！
echo ========================================
echo.
echo 已安裝的套件：
echo - Django 3.2.9
echo - firebase-admin
echo - mysqlclient
echo.
pause


