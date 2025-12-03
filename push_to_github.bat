@echo off
chcp 65001 >nul
echo ========================================
echo 推送 CampingData 專案到 GitHub
echo ========================================
echo.
echo ⚠️  首次推送需要 GitHub 認證
echo    如果尚未設定認證，請先執行：quick_auth_setup.bat
echo    或查看：GITHUB_AUTHENTICATION.md
echo.
pause

REM 檢查是否在正確的目錄
if not exist "manage.py" (
    echo 錯誤：請在專案根目錄執行此腳本
    pause
    exit /b 1
)

REM 初始化 Git（如果尚未初始化）
if not exist ".git" (
    echo 初始化 Git 倉庫...
    git init
    if errorlevel 1 (
        echo 錯誤：無法初始化 Git 倉庫，請確認已安裝 Git
        pause
        exit /b 1
    )
)

REM 設置遠程倉庫
echo 設置遠程倉庫...
git remote remove origin 2>nul
git remote add origin https://github.com/rurumi02-boop/CampingData.git
if errorlevel 1 (
    echo 警告：設置遠程倉庫時出現問題，可能已存在
)

REM 添加所有文件
echo 添加文件到暫存區...
git add .
if errorlevel 1 (
    echo 錯誤：無法添加文件
    pause
    exit /b 1
)

REM 提交更改
echo 提交更改...
git commit -m "Initial commit: CampingData Django e-commerce project"
if errorlevel 1 (
    echo 警告：提交時出現問題，可能沒有變更需要提交
)

REM 推送到主分支
echo 推送到 GitHub...
echo.
echo 如果這是首次推送，系統會要求您輸入認證資訊：
echo   - Username: 輸入您的 GitHub 使用者名稱
echo   - Password: 輸入您的 Personal Access Token（不是 GitHub 密碼！）
echo.
echo 如果尚未創建 Token，請：
echo   1. 前往：https://github.com/settings/tokens/new
echo   2. 勾選 'repo' 權限
echo   3. 生成並複製 Token
echo.
pause
git branch -M main
git push -u origin main
if errorlevel 1 (
    echo.
    echo ========================================
    echo ❌ 推送失敗
    echo ========================================
    echo.
    echo 可能的原因：
    echo 1. 認證失敗 - 請確認 Token 正確
    echo 2. 倉庫不存在 - 請確認已創建 GitHub 倉庫
    echo 3. 權限不足 - 請確認 Token 有 'repo' 權限
    echo.
    echo 解決方法：
    echo 1. 執行 quick_auth_setup.bat 重新設定認證
    echo 2. 查看 GITHUB_AUTHENTICATION.md 了解詳細步驟
    echo 3. 手動執行：git push -u origin main
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo 推送完成！
echo ========================================
pause

