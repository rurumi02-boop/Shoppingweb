@echo off
chcp 65001 >nul
title 安裝 Python 3.11 指南
color 0B

echo.
echo ========================================
echo   安裝 Python 3.11 完整指南
echo ========================================
echo.
echo 這將解決 Python 3.14 與 Django 3.2.9 的相容性問題
echo.
pause

echo.
echo ========================================
echo   步驟 1：下載 Python 3.11
echo ========================================
echo.
echo 請前往以下網址下載：
echo https://www.python.org/downloads/release/python-3110/
echo.
echo 選擇：Windows installer (64-bit)
echo 檔案名稱：python-3.11.0-amd64.exe
echo.
echo 是否要現在開啟下載頁面？
choice /C YN /M "開啟瀏覽器下載 Python 3.11"
if errorlevel 2 goto skip_download
if errorlevel 1 start https://www.python.org/downloads/release/python-3110/

:skip_download
echo.
echo ========================================
echo   步驟 2：安裝 Python 3.11
echo ========================================
echo.
echo ⚠️  重要提醒：
echo.
echo 1. 執行下載的 python-3.11.0-amd64.exe
echo 2. 務必勾選「Add Python 3.11 to PATH」
echo 3. 選擇「Install Now」
echo 4. 等待安裝完成
echo.
pause

echo.
echo ========================================
echo   步驟 3：驗證安裝
echo ========================================
echo.
echo 安裝完成後，請：
echo 1. 關閉當前 PowerShell 視窗
echo 2. 重新開啟一個新的 PowerShell
echo 3. 執行以下命令驗證：
echo.
echo    python --version
echo    （應該顯示：Python 3.11.0）
echo.
pause

echo.
echo ========================================
echo   步驟 4：重新安裝依賴
echo ========================================
echo.
echo 在新的 PowerShell 中執行：
echo.
echo    cd C:\CampingData
echo    pip install -r requirements.txt
echo.
pause

echo.
echo ========================================
echo   步驟 5：測試專案
echo ========================================
echo.
echo 執行以下命令測試：
echo.
echo    python manage.py check
echo    （應該不會再看到 cgi 模組錯誤）
echo.
echo    python manage.py runserver
echo    （啟動開發伺服器）
echo.
echo ========================================
echo   完成！
echo ========================================
echo.
pause

