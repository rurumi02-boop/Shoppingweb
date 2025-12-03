# 推送 CampingData 到 GitHub
# 此腳本會自動尋找 Git 並執行推送

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "推送 CampingData 專案到 GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 檢查是否在正確的目錄
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ 錯誤：請在專案根目錄執行此腳本" -ForegroundColor Red
    Write-Host "當前目錄：$PWD" -ForegroundColor Yellow
    Read-Host "按 Enter 鍵退出"
    exit 1
}

# 嘗試找到 Git
$gitPath = $null
$possiblePaths = @(
    "git",
    "C:\Program Files\Git\bin\git.exe",
    "C:\Program Files (x86)\Git\bin\git.exe",
    "$env:LOCALAPPDATA\Programs\Git\bin\git.exe",
    "$env:USERPROFILE\AppData\Local\Programs\Git\bin\git.exe"
)

foreach ($path in $possiblePaths) {
    try {
        if ($path -eq "git") {
            $result = & git --version 2>$null
            if ($result) {
                $gitPath = "git"
                break
            }
        } else {
            if (Test-Path $path) {
                $result = & $path --version 2>$null
                if ($result) {
                    $gitPath = $path
                    break
                }
            }
        }
    } catch {
        continue
    }
}

if (-not $gitPath) {
    Write-Host "❌ 錯誤：未找到 Git！" -ForegroundColor Red
    Write-Host ""
    Write-Host "可能的原因：" -ForegroundColor Yellow
    Write-Host "1. Git 未安裝" -ForegroundColor White
    Write-Host "2. Git 未加入 PATH 環境變數" -ForegroundColor White
    Write-Host "3. 需要重新啟動 PowerShell" -ForegroundColor White
    Write-Host ""
    Write-Host "解決方法：" -ForegroundColor Yellow
    Write-Host "1. 確認 Git 已安裝" -ForegroundColor White
    Write-Host "2. 重新啟動 PowerShell（關閉並重新開啟）" -ForegroundColor White
    Write-Host "3. 或查看「手動推送命令.txt」使用完整路徑" -ForegroundColor White
    Write-Host ""
    Read-Host "按 Enter 鍵退出"
    exit 1
}

Write-Host "✅ 找到 Git：$gitPath" -ForegroundColor Green
Write-Host ""

# Token 和倉庫設定
$TOKEN = "YOUR_GITHUB_TOKEN_HERE"
$USERNAME = "rurumi02-boop"
$REPO = "CampingData"
$REPO_URL = "https://${TOKEN}@github.com/${USERNAME}/${REPO}.git"

Write-Host "📦 遠程倉庫：https://github.com/$USERNAME/$REPO" -ForegroundColor Cyan
Write-Host ""

# 初始化 Git（如果尚未初始化）
if (-not (Test-Path ".git")) {
    Write-Host "[步驟 1/6] 初始化 Git 倉庫..." -ForegroundColor Yellow
    & $gitPath init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 錯誤：無法初始化 Git 倉庫" -ForegroundColor Red
        Read-Host "按 Enter 鍵退出"
        exit 1
    }
    Write-Host "✅ Git 倉庫初始化完成" -ForegroundColor Green
} else {
    Write-Host "✅ Git 倉庫已存在" -ForegroundColor Green
}

Write-Host ""

# 設置遠程倉庫
Write-Host "[步驟 2/6] 設置遠程倉庫..." -ForegroundColor Yellow
& $gitPath remote remove origin 2>$null
& $gitPath remote add origin $REPO_URL
if ($LASTEXITCODE -ne 0) {
    & $gitPath remote set-url origin $REPO_URL
}
Write-Host "✅ 遠程倉庫設置完成" -ForegroundColor Green
Write-Host ""

# 添加所有文件
Write-Host "[步驟 3/6] 添加文件到暫存區..." -ForegroundColor Yellow
& $gitPath add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 錯誤：無法添加文件" -ForegroundColor Red
    Read-Host "按 Enter 鍵退出"
    exit 1
}
Write-Host "✅ 文件已添加到暫存區" -ForegroundColor Green
Write-Host ""

# 提交更改
Write-Host "[步驟 4/6] 提交更改..." -ForegroundColor Yellow
& $gitPath commit -m "Initial commit: CampingData Django e-commerce project"
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  警告：提交時出現問題，可能沒有變更需要提交" -ForegroundColor Yellow
    Write-Host "繼續執行推送..." -ForegroundColor Yellow
}
Write-Host ""

# 設定主分支
Write-Host "[步驟 5/6] 設定主分支..." -ForegroundColor Yellow
& $gitPath branch -M main
Write-Host "✅ 主分支設定完成" -ForegroundColor Green
Write-Host ""

# 推送到 GitHub
Write-Host "[步驟 6/6] 推送到 GitHub..." -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  如果這是首次推送，可能需要幾秒鐘時間..." -ForegroundColor Yellow
Write-Host ""
& $gitPath push -u origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "❌ 推送失敗" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "可能的原因：" -ForegroundColor Yellow
    Write-Host "1. Token 無效或已過期" -ForegroundColor White
    Write-Host "2. 倉庫不存在或無權限" -ForegroundColor White
    Write-Host "3. 網路連接問題" -ForegroundColor White
    Write-Host ""
    Write-Host "請檢查：" -ForegroundColor Yellow
    Write-Host "- GitHub 倉庫是否已創建：https://github.com/$USERNAME/$REPO" -ForegroundColor White
    Write-Host "- Token 是否有 'repo' 權限" -ForegroundColor White
    Write-Host "- 網路連接是否正常" -ForegroundColor White
    Write-Host ""
    Read-Host "按 Enter 鍵退出"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ 推送成功！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "您的專案已成功推送到：" -ForegroundColor Cyan
Write-Host "https://github.com/$USERNAME/$REPO" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  重要安全提醒：" -ForegroundColor Red
Write-Host "   1. Token 已保存在本地 Git 配置中" -ForegroundColor Yellow
Write-Host "   2. 建議到 GitHub 撤銷此 Token 並生成新的" -ForegroundColor Yellow
Write-Host "   3. 前往：https://github.com/settings/tokens" -ForegroundColor Yellow
Write-Host ""
Read-Host "按 Enter 鍵退出"


