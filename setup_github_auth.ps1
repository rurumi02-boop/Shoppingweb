# GitHub 認證設定腳本
# 此腳本幫助您設定 GitHub 認證

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub 認證設定助手" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 檢查 Git 是否安裝
$gitPath = $null
$possiblePaths = @(
    "C:\Program Files\Git\bin\git.exe",
    "C:\Program Files (x86)\Git\bin\git.exe",
    "git"
)

foreach ($path in $possiblePaths) {
    try {
        if ($path -eq "git") {
            $gitVersion = & git --version 2>$null
            if ($gitVersion) {
                $gitPath = "git"
                break
            }
        } else {
            if (Test-Path $path) {
                $gitPath = $path
                break
            }
        }
    } catch {
        continue
    }
}

if (-not $gitPath) {
    Write-Host "❌ 錯誤：未找到 Git，請先安裝 Git" -ForegroundColor Red
    Write-Host "下載地址：https://git-scm.com/download/win" -ForegroundColor Yellow
    Read-Host "按 Enter 鍵退出"
    exit 1
}

Write-Host "✅ 找到 Git：$gitPath" -ForegroundColor Green
Write-Host ""

# 選擇認證方式
Write-Host "請選擇認證方式：" -ForegroundColor Yellow
Write-Host "1. 使用 Personal Access Token (PAT) - 推薦" -ForegroundColor White
Write-Host "2. 使用 SSH 金鑰 - 最安全" -ForegroundColor White
Write-Host "3. 查看詳細說明文件" -ForegroundColor White
Write-Host "4. 退出" -ForegroundColor White
Write-Host ""

$choice = Read-Host "請輸入選項 (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "=== 使用 Personal Access Token ===" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "請按照以下步驟操作：" -ForegroundColor Yellow
        Write-Host "1. 開啟瀏覽器，前往：https://github.com/settings/tokens" -ForegroundColor White
        Write-Host "2. 點擊 'Generate new token' → 'Generate new token (classic)'" -ForegroundColor White
        Write-Host "3. 填寫 Note（例如：CampingData Project）" -ForegroundColor White
        Write-Host "4. 選擇過期時間" -ForegroundColor White
        Write-Host "5. 勾選 'repo' 權限" -ForegroundColor White
        Write-Host "6. 點擊 'Generate token'" -ForegroundColor White
        Write-Host "7. 複製生成的 Token（只會顯示一次！）" -ForegroundColor Red
        Write-Host ""
        
        $openBrowser = Read-Host "是否要現在開啟瀏覽器到 Token 創建頁面？(Y/N)"
        if ($openBrowser -eq "Y" -or $openBrowser -eq "y") {
            Start-Process "https://github.com/settings/tokens/new"
        }
        
        Write-Host ""
        Write-Host "請輸入您的 GitHub 使用者名稱：" -ForegroundColor Yellow
        $username = Read-Host
        
        Write-Host ""
        Write-Host "請貼上您的 Personal Access Token：" -ForegroundColor Yellow
        $token = Read-Host -AsSecureString
        $tokenPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
            [Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
        )
        
        # 設定遠程 URL（包含 Token）
        $remoteUrl = "https://${tokenPlain}@github.com/rurumi02-boop/CampingData.git"
        
        Write-Host ""
        Write-Host "正在設定遠程倉庫..." -ForegroundColor Yellow
        & git remote remove origin 2>$null
        & git remote add origin $remoteUrl
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ 遠程倉庫設定成功！" -ForegroundColor Green
            Write-Host ""
            Write-Host "⚠️  注意：Token 已保存在 Git 配置中" -ForegroundColor Yellow
            Write-Host "建議之後改用 SSH 金鑰以提高安全性" -ForegroundColor Yellow
        } else {
            Write-Host "❌ 設定失敗，請檢查 Token 是否正確" -ForegroundColor Red
        }
    }
    
    "2" {
        Write-Host ""
        Write-Host "=== 使用 SSH 金鑰 ===" -ForegroundColor Cyan
        Write-Host ""
        
        # 檢查是否已有 SSH 金鑰
        $sshKeyPath = "$env:USERPROFILE\.ssh\id_ed25519.pub"
        if (Test-Path $sshKeyPath) {
            Write-Host "✅ 發現現有的 SSH 公鑰" -ForegroundColor Green
            Write-Host ""
            Write-Host "您的公鑰內容：" -ForegroundColor Yellow
            Get-Content $sshKeyPath
            Write-Host ""
            Write-Host "請將上述公鑰添加到 GitHub：" -ForegroundColor Yellow
            Write-Host "1. 前往：https://github.com/settings/keys" -ForegroundColor White
            Write-Host "2. 點擊 'New SSH key'" -ForegroundColor White
            Write-Host "3. 貼上上述公鑰內容" -ForegroundColor White
            Write-Host ""
            
            $openBrowser = Read-Host "是否要現在開啟瀏覽器到 SSH 金鑰頁面？(Y/N)"
            if ($openBrowser -eq "Y" -or $openBrowser -eq "y") {
                Start-Process "https://github.com/settings/keys"
            }
            
            $continue = Read-Host "完成後按 Enter 繼續"
        } else {
            Write-Host "未找到 SSH 金鑰，正在生成..." -ForegroundColor Yellow
            Write-Host ""
            Write-Host "請輸入您的 Email（用於 SSH 金鑰）：" -ForegroundColor Yellow
            $email = Read-Host
            
            Write-Host ""
            Write-Host "正在生成 SSH 金鑰..." -ForegroundColor Yellow
            & ssh-keygen -t ed25519 -C $email -f "$env:USERPROFILE\.ssh\id_ed25519" -N '""'
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ SSH 金鑰生成成功！" -ForegroundColor Green
                Write-Host ""
                Write-Host "您的公鑰內容：" -ForegroundColor Yellow
                Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub"
                Write-Host ""
                Write-Host "請將上述公鑰添加到 GitHub：" -ForegroundColor Yellow
                Write-Host "1. 前往：https://github.com/settings/keys" -ForegroundColor White
                Write-Host "2. 點擊 'New SSH key'" -ForegroundColor White
                Write-Host "3. 貼上上述公鑰內容" -ForegroundColor White
                Write-Host ""
                
                $openBrowser = Read-Host "是否要現在開啟瀏覽器到 SSH 金鑰頁面？(Y/N)"
                if ($openBrowser -eq "Y" -or $openBrowser -eq "y") {
                    Start-Process "https://github.com/settings/keys"
                }
                
                $continue = Read-Host "完成後按 Enter 繼續"
            } else {
                Write-Host "❌ SSH 金鑰生成失敗" -ForegroundColor Red
                Read-Host "按 Enter 鍵退出"
                exit 1
            }
        }
        
        # 設定 SSH 遠程 URL
        Write-Host ""
        Write-Host "正在設定 SSH 遠程倉庫..." -ForegroundColor Yellow
        & git remote remove origin 2>$null
        & git remote add origin "git@github.com:rurumi02-boop/CampingData.git"
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ SSH 遠程倉庫設定成功！" -ForegroundColor Green
            Write-Host ""
            Write-Host "測試 SSH 連接..." -ForegroundColor Yellow
            & ssh -T git@github.com 2>&1
        } else {
            Write-Host "❌ 設定失敗" -ForegroundColor Red
        }
    }
    
    "3" {
        Write-Host ""
        Write-Host "正在開啟說明文件..." -ForegroundColor Yellow
        if (Test-Path "GITHUB_AUTHENTICATION.md") {
            Start-Process "GITHUB_AUTHENTICATION.md"
        } else {
            Write-Host "說明文件不存在" -ForegroundColor Red
        }
    }
    
    "4" {
        Write-Host "退出" -ForegroundColor Yellow
        exit 0
    }
    
    default {
        Write-Host "無效的選項" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "設定完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "現在您可以執行推送命令：" -ForegroundColor Yellow
Write-Host "  git add ." -ForegroundColor White
Write-Host "  git commit -m 'Initial commit'" -ForegroundColor White
Write-Host "  git push -u origin main" -ForegroundColor White
Write-Host ""
Read-Host "按 Enter 鍵退出"


