@echo off
chcp 65001 >nul
echo ========================================
echo GitHub 認證快速設定
echo ========================================
echo.
echo 此腳本將引導您完成 GitHub 認證設定
echo.
pause

powershell -ExecutionPolicy Bypass -File "setup_github_auth.ps1"

pause


