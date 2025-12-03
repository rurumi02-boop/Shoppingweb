# GitHub 認證指南

## 方法一：使用 Personal Access Token (PAT) - 推薦

### 步驟 1：創建 Personal Access Token

1. 登入 GitHub 帳號
2. 點擊右上角頭像 → **Settings**（設定）
3. 左側選單最下方點擊 **Developer settings**
4. 點擊 **Personal access tokens** → **Tokens (classic)**
5. 點擊 **Generate new token** → **Generate new token (classic)**
6. 填寫資訊：
   - **Note**（備註）：例如 "CampingData Project"
   - **Expiration**（過期時間）：選擇適合的期限（建議 90 天或自訂）
   - **Select scopes**（選擇權限）：至少勾選以下項目：
     - ✅ `repo`（完整倉庫權限）
     - ✅ `workflow`（如果需要 GitHub Actions）
7. 點擊 **Generate token**
8. **重要**：複製生成的 Token（只會顯示一次！）
   - 格式類似：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 步驟 2：使用 Token 進行認證

#### 方式 A：在推送時輸入（一次性）

當執行 `git push` 時：
- **Username**：輸入你的 GitHub 使用者名稱
- **Password**：**貼上剛才複製的 Token**（不是 GitHub 密碼！）

#### 方式 B：使用 Git Credential Manager（推薦，永久保存）

Windows 系統通常已安裝 Git Credential Manager，執行推送時會自動彈出視窗要求輸入。

#### 方式 C：在 URL 中嵌入 Token（不推薦，但簡單）

```bash
git remote set-url origin https://YOUR_TOKEN@github.com/rurumi02-boop/CampingData.git
```

將 `YOUR_TOKEN` 替換為你的 Personal Access Token。

⚠️ **注意**：這種方式會將 Token 保存在 Git 配置中，安全性較低。

#### 方式 D：使用環境變數（推薦用於腳本）

在 PowerShell 中：
```powershell
$env:GIT_ASKPASS = "echo"
git -c credential.helper='!f() { echo "username=YOUR_USERNAME"; echo "password=YOUR_TOKEN"; }; f' push origin main
```

## 方法二：使用 SSH 金鑰（最安全，推薦長期使用）

### 步驟 1：生成 SSH 金鑰

在 PowerShell 或 Git Bash 中執行：

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

- 按 Enter 使用預設位置（通常是 `C:\Users\YourName\.ssh\id_ed25519`）
- 可選擇設定密碼（建議設定）

### 步驟 2：複製公鑰

```bash
cat ~/.ssh/id_ed25519.pub
```

或使用 PowerShell：
```powershell
Get-Content ~/.ssh/id_ed25519.pub
```

複製輸出的完整內容（從 `ssh-ed25519` 開始到結尾）。

### 步驟 3：添加到 GitHub

1. GitHub → Settings → **SSH and GPG keys**
2. 點擊 **New SSH key**
3. **Title**：例如 "My Windows PC"
4. **Key**：貼上剛才複製的公鑰
5. 點擊 **Add SSH key**

### 步驟 4：更改遠程 URL 為 SSH

```bash
git remote set-url origin git@github.com:rurumi02-boop/CampingData.git
```

之後推送就不需要輸入密碼了。

## 方法三：使用 GitHub Desktop（最簡單）

1. 下載安裝 GitHub Desktop：https://desktop.github.com/
2. 登入 GitHub 帳號
3. 在 GitHub Desktop 中：
   - File → Add Local Repository
   - 選擇 `C:\CampingData`
   - 點擊 Publish repository

## 方法四：使用 GitHub CLI

### 安裝 GitHub CLI

```powershell
# 使用 Chocolatey
choco install gh

# 或使用 Scoop
scoop install gh
```

### 登入

```bash
gh auth login
```

按照提示選擇：
- GitHub.com
- HTTPS
- 認證方式（瀏覽器或 Token）

## 驗證認證是否成功

執行以下命令測試：

```bash
# 測試 HTTPS 連接
git ls-remote https://github.com/rurumi02-boop/CampingData.git

# 測試 SSH 連接（如果使用 SSH）
ssh -T git@github.com
```

## 常見問題

### Q: 推送時出現 "Authentication failed"
**A:** 
- 確認 Token 是否正確複製（沒有多餘空格）
- 確認 Token 是否已過期
- 確認是否有 `repo` 權限

### Q: 如何更新已保存的認證資訊？
**A:** 
在 Windows 中：
1. 控制台 → 認證管理員 → Windows 認證
2. 找到 `git:https://github.com`
3. 編輯或刪除後重新認證

### Q: Token 忘記了怎麼辦？
**A:** 
1. GitHub → Settings → Developer settings → Personal access tokens
2. 找到對應的 Token，可以重新生成或刪除舊的

### Q: 如何撤銷 Token？
**A:** 
在 Personal access tokens 頁面，點擊 Token 右側的垃圾桶圖示刪除。

## 安全建議

1. ✅ **使用 Personal Access Token 而非密碼**
2. ✅ **定期更新 Token**
3. ✅ **為不同專案使用不同的 Token**
4. ✅ **不要將 Token 提交到 Git 倉庫**
5. ✅ **使用 SSH 金鑰（長期專案推薦）**
6. ❌ **不要在公開場所分享 Token**


