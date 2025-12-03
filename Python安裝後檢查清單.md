# Python 3.14.0 安裝後檢查清單

## ✅ 安裝完成！

您已成功安裝 Python 3.14.0。以下是安裝後需要注意的事項：

## 🔍 立即檢查步驟

### 1. 重新開啟命令提示字元（重要！）

**⚠️ 必須執行**：關閉當前的命令提示字元或 PowerShell，然後重新開啟一個新的。

這是因為 PATH 環境變數的變更需要重新載入終端才能生效。

### 2. 驗證 Python 安裝

在新的命令提示字元中執行：

```bash
python --version
```

應該顯示：`Python 3.14.0`

### 3. 驗證 pip 安裝

```bash
pip --version
```

應該顯示 pip 的版本號（例如：`pip 24.x.x`）

### 4. 驗證 py 啟動器

```bash
py --version
```

應該顯示：`Python 3.14.0`

## 📦 安裝專案依賴

在專案目錄（`C:\CampingData`）執行：

```bash
cd C:\CampingData
pip install -r requirements.txt
```

這會安裝：
- Django 3.2.9
- firebase-admin
- mysqlclient

## ⚙️ 關於安裝對話框中的選項

### "Disable path length limit" 選項

如果您還沒關閉安裝對話框，可以考慮點擊「Disable path length limit」：

**優點**：
- 允許程式（包括 Python）繞過 Windows 的 260 字元路徑長度限制
- 對於深度嵌套的專案很有用

**注意**：
- 這會修改系統配置
- 需要管理員權限
- 對於大多數專案不是必需的

**建議**：
- 如果您的專案路徑較短（如 `C:\CampingData`），可以不勾選
- 如果未來可能遇到路徑過長的問題，可以現在勾選

## 🚀 下一步操作

### 1. 安裝專案依賴

```bash
# 確保在專案目錄
cd C:\CampingData

# 安裝依賴
pip install -r requirements.txt
```

### 2. 設定 Firebase（如果使用 Firebase 分支）

1. 下載 Firebase 憑證檔案
2. 重命名為 `firebase-credentials.json`
3. 放在專案根目錄

### 3. 測試 Django 專案

```bash
# 執行資料庫遷移（如果使用 MySQL）
python manage.py migrate

# 啟動開發伺服器
python manage.py runserver
```

## ❓ 常見問題

### Q: 執行 `python --version` 還是顯示錯誤
**A:** 
- 確認已重新開啟命令提示字元
- 確認安裝時勾選了「Add Python to PATH」
- 嘗試使用 `py --version`

### Q: 執行 `pip install` 時出現權限錯誤
**A:** 
- 使用 `pip install --user -r requirements.txt`（安裝到使用者目錄）
- 或以系統管理員身分執行命令提示字元

### Q: 安裝依賴時出現錯誤
**A:** 
- 檢查網路連接
- 嘗試使用 `pip install -r requirements.txt --upgrade`
- 查看具體錯誤訊息

## ✅ 驗證清單

安裝完成後，確認以下項目：

- [ ] 已重新開啟命令提示字元
- [ ] `python --version` 可以執行並顯示版本
- [ ] `pip --version` 可以執行並顯示版本
- [ ] 已安裝專案依賴（`pip install -r requirements.txt`）
- [ ] 沒有錯誤訊息

## 🎉 完成！

如果以上步驟都成功，您就可以開始使用 Python 和 Django 專案了！


