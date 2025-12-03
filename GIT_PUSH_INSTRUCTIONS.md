# Git 推送指南

## 前置準備
1. 確保已安裝 Git：https://git-scm.com/download/win
2. 確保已設定 Git 使用者資訊：
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

## 推送步驟

在專案根目錄（C:\CampingData）執行以下命令：

### 1. 初始化 Git 倉庫（如果尚未初始化）
```bash
git init
```

### 2. 添加遠程倉庫
```bash
git remote add origin https://github.com/rurumi02-boop/CampingData.git
```

如果遠程倉庫已存在，使用：
```bash
git remote set-url origin https://github.com/rurumi02-boop/CampingData.git
```

### 3. 添加所有文件
```bash
git add .
```

### 4. 提交更改
```bash
git commit -m "Initial commit: CampingData Django e-commerce project"
```

### 5. 推送到主分支
```bash
git branch -M main
git push -u origin main
```

如果遠程倉庫使用 `master` 分支：
```bash
git branch -M master
git push -u origin master
```

## 注意事項
- 確保 `.gitignore` 已正確設置，避免提交敏感資訊（如資料庫、密碼等）
- 如果遇到認證問題，可能需要設定 GitHub Personal Access Token
- 如果倉庫已存在內容，可能需要先執行 `git pull` 合併遠程更改


