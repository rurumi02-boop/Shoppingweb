# 使用 Token 推送專案到 GitHub

## ⚠️ 重要：系統需要先安裝 Git

如果系統提示「未找到 Git」，請先安裝：
- 下載地址：https://git-scm.com/download/win
- 安裝時選擇「Add Git to PATH」選項

## 使用提供的 Token 推送

您的 Token 已配置在以下腳本中：
- `push_with_token.bat` - Windows 批次檔
- `push_with_token.ps1` - PowerShell 腳本

### 方法一：使用批次檔（推薦）

1. 確保已安裝 Git
2. 雙擊執行 `push_with_token.bat`
3. 腳本會自動：
   - 初始化 Git 倉庫（如果尚未初始化）
   - 設定遠程倉庫
   - 添加所有文件
   - 提交更改
   - 推送到 GitHub

### 方法二：使用 PowerShell 腳本

1. 確保已安裝 Git
2. 在專案目錄開啟 PowerShell
3. 執行：
   ```powershell
   powershell -ExecutionPolicy Bypass -File "push_with_token.ps1"
   ```

### 方法三：手動執行命令

如果腳本無法執行，可以手動執行以下命令：

```bash
# 1. 初始化 Git（如果尚未初始化）
git init

# 2. 設定遠程倉庫（使用 Token）
git remote add origin https://YOUR_GITHUB_TOKEN_HERE@github.com/rurumi02-boop/CampingData.git

# 如果遠程倉庫已存在，使用：
# git remote set-url origin https://YOUR_GITHUB_TOKEN_HERE@github.com/rurumi02-boop/CampingData.git

# 3. 添加所有文件
git add .

# 4. 提交更改
git commit -m "Initial commit: CampingData Django e-commerce project"

# 5. 推送到主分支
git branch -M main
git push -u origin main
```

## 安全提醒

⚠️ **重要**：Token 已暴露在對話中，建議：

1. **推送完成後立即撤銷此 Token**：
   - 前往：https://github.com/settings/tokens
   - 找到對應的 Token 並刪除

2. **生成新的 Token**：
   - 創建新的 Personal Access Token
   - 更新本地 Git 配置

3. **不要提交包含 Token 的文件**：
   - `setup_token.bat`
   - `push_with_token.bat`
   - `push_with_token.ps1`
   
   這些文件已在 `.gitignore` 中排除

## 驗證推送是否成功

推送完成後，訪問以下網址確認：
https://github.com/rurumi02-boop/CampingData

## 常見問題

### Q: 提示「未找到 Git」
**A:** 請先安裝 Git：https://git-scm.com/download/win

### Q: 推送失敗，提示認證錯誤
**A:** 
- 確認 Token 是否正確
- 確認 Token 是否有 `repo` 權限
- 確認 GitHub 倉庫是否已創建

### Q: 推送失敗，提示倉庫不存在
**A:** 
- 前往 https://github.com/new 創建新倉庫
- 倉庫名稱：`CampingData`
- 選擇 Public 或 Private

### Q: 如何更新 Token？
**A:** 
1. 生成新的 Token
2. 更新遠程 URL：
   ```bash
   git remote set-url origin https://NEW_TOKEN@github.com/rurumi02-boop/CampingData.git
   ```


