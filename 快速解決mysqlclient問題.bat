@echo off
chcp 65001 >nul
title 安裝 PyMySQL（替代 mysqlclient）
color 0B

echo.
echo ========================================
echo   安裝 PyMySQL（替代 mysqlclient）
echo ========================================
echo.
echo PyMySQL 優點：
echo - 不需要編譯
echo - 不需要 C++ Build Tools
echo - 安裝快速簡單
echo - 功能與 mysqlclient 相同
echo.
pause

echo.
echo 正在安裝 PyMySQL...
python -m pip install PyMySQL

if errorlevel 1 (
    echo.
    echo [❌] 安裝失敗
    echo 請檢查 Python 和 pip 是否正確安裝
    pause
    exit /b 1
)

echo.
echo ========================================
echo [✅] PyMySQL 安裝成功！
echo ========================================
echo.
echo 下一步：
echo 1. 如果使用 MySQL，需要在 settings.py 中添加：
echo    import pymysql
echo    pymysql.install_as_MySQLdb()
echo.
echo 2. 驗證安裝：
echo    python -c "import pymysql; print('PyMySQL 安裝成功！')"
echo.
pause


