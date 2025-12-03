# 安裝 Python 3.11 完整指南

## 方案一：降級到 Python 3.11

這是最穩定且推薦的解決方案，與 Django 3.2.9 完全相容。

## 步驟 1：下載 Python 3.11

### 方法一：官方網站下載（推薦）

1. **前往 Python 官方網站**
   - 網址：https://www.python.org/downloads/release/python-3110/
   - 或直接搜尋「Python 3.11.0 download」

2. **選擇下載檔案**
   - 找到「Windows installer (64-bit)」
   - 檔案名稱：`python-3.11.0-amd64.exe`
   - 檔案大小：約 25-30 MB

3. **點擊下載**

### 方法二：直接下載連結

- **Windows 64-bit**：https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe

## 步驟 2：安裝 Python 3.11

### 安裝步驟

1. **執行安裝程式**
   - 雙擊下載的 `python-3.11.0-amd64.exe`

2. **安裝選項**
   - ⚠️ **非常重要**：勾選「**Add Python 3.11 to PATH**」
   - 選擇「Install Now」（推薦）
   - 或選擇「Customize installation」進行自訂安裝

3. **等待安裝完成**
   - 安裝過程約需 1-3 分鐘
   - 看到「Setup was successful」表示安裝完成

4. **點擊「Close」關閉安裝程式**

## 步驟 3：驗證安裝

### 重新開啟 PowerShell

**重要**：必須關閉當前 PowerShell 視窗，重新開啟一個新的，PATH 才會生效。

### 驗證命令

在新的 PowerShell 中執行：

```powershell
# 檢查 Python 版本
python --version
# 應該顯示：Python 3.11.0

# 檢查 pip 版本
pip --version
# 應該顯示 pip 版本和 Python 3.11

# 檢查 Python 路徑
where.exe python
# 應該顯示 Python 3.11 的路徑
```

## 步驟 4：重新安裝專案依賴

### 切換到專案目錄

```powershell
cd C:\CampingData
```

### 重新安裝依賴

```powershell
# 安裝所有專案依賴
pip install -r requirements.txt
```

這會安裝：
- Django 3.2.9
- firebase-admin
- PyMySQL

## 步驟 5：驗證所有設定

### 驗證依賴安裝

```powershell
# 檢查 Django
python -c "import django; print('✅ Django 版本：', django.get_version())"

# 檢查 Firebase
python -c "import firebase_admin; print('✅ Firebase Admin SDK: 已安裝')"

# 檢查 PyMySQL
python -c "import pymysql; print('✅ PyMySQL 版本：', pymysql.__version__)"
```

### 測試 Django 專案

```powershell
# 檢查 Django 設定
python manage.py check

# 應該不會再看到 cgi 模組錯誤
```

### 測試 Firebase 連接

```powershell
python -c "from firebase_admin import firestore; db = firestore.client(); print('✅ Firebase 連接成功')"
```

## 步驟 6：啟動開發伺服器

如果所有驗證都通過，可以啟動開發伺服器：

```powershell
python manage.py runserver
```

然後在瀏覽器中訪問：http://127.0.0.1:8000/

## 完整操作流程

```
1. 下載 Python 3.11.0
   ↓
2. 執行安裝程式
   ↓
3. 勾選「Add Python 3.11 to PATH」
   ↓
4. 完成安裝
   ↓
5. 關閉並重新開啟 PowerShell
   ↓
6. 驗證：python --version（應該顯示 3.11.0）
   ↓
7. 切換到專案目錄：cd C:\CampingData
   ↓
8. 重新安裝依賴：pip install -r requirements.txt
   ↓
9. 測試：python manage.py check
   ↓
10. 啟動伺服器：python manage.py runserver
```

## 常見問題

### Q: 安裝後 `python --version` 還是顯示 3.14？
**A:** 
- 確認已重新開啟 PowerShell（關閉並重新開啟）
- 檢查 PATH：`$env:PATH -split ';' | Select-String Python`
- 確認 Python 3.11 的路徑在 PATH 中

### Q: 如何確認使用的是 Python 3.11？
**A:** 
```powershell
# 檢查 Python 路徑
where.exe python

# 應該顯示類似：C:\Users\您的使用者名稱\AppData\Local\Programs\Python\Python311\python.exe
```

### Q: 可以同時安裝多個 Python 版本嗎？
**A:** 
- 可以，Windows 可以同時安裝多個 Python 版本
- 使用 `py` launcher 可以選擇版本：
  ```powershell
  py -3.11 --version  # Python 3.11
  py -3.14 --version  # Python 3.14
  ```

### Q: 如果安裝時忘記勾選「Add to PATH」？
**A:** 
1. 重新執行 Python 3.11 安裝程式
2. 選擇「Modify」
3. 勾選「Add Python 3.11 to PATH」
4. 或手動加入 PATH 環境變數

## 驗證清單

完成後，確認以下項目：

- [ ] Python 3.11 已安裝
- [ ] `python --version` 顯示 3.11.0
- [ ] `pip --version` 正常
- [ ] 已重新安裝所有依賴
- [ ] `python manage.py check` 沒有錯誤
- [ ] Firebase 可以正常連接

## 下一步

安裝完成後：
1. 驗證所有依賴已安裝
2. 測試 Django 專案
3. 啟動開發伺服器
4. 測試 Firebase 功能

## 參考

- Python 3.11 下載：https://www.python.org/downloads/release/python-3110/
- Django 版本相容性：見 `Django版本與Python314支援情況.md`

