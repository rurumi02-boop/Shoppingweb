# 使用 Python 3.11 運行專案

## 當前狀況

✅ **Python 3.11 已成功安裝**
✅ **所有依賴已安裝**
✅ **遷移檔案已修復**

⚠️ **但是**：`python` 命令仍指向 Python 3.14（因為 PATH 順序）

## 解決方案

### 方法一：使用 py launcher（推薦）⭐

使用 `py -3.11` 來明確指定使用 Python 3.11：

```powershell
# 檢查版本
py -3.11 --version
# 應該顯示：Python 3.11.0

# 檢查 Django
py -3.11 manage.py check

# 啟動開發伺服器
py -3.11 manage.py runserver
```

### 方法二：調整 PATH 環境變數

讓 Python 3.11 優先於 Python 3.14：

1. **找到 Python 3.11 的路徑**
   ```powershell
   py -3.11 -c "import sys; print(sys.executable)"
   ```
   通常類似：`C:\Users\您的使用者名稱\AppData\Local\Programs\Python\Python311\python.exe`

2. **調整 PATH**
   - 右鍵「此電腦」→「內容」→「進階系統設定」
   - 點擊「環境變數」
   - 在「系統變數」中找到「Path」，點擊「編輯」
   - 將 Python 3.11 的路徑移到 Python 3.14 之前
   - 或刪除 Python 3.14 的路徑（如果不需要）

3. **重新開啟 PowerShell**

## 完整操作命令

### 使用 Python 3.11 運行專案

```powershell
# 1. 切換到專案目錄
cd C:\CampingData

# 2. 檢查 Django（使用 Python 3.11）
py -3.11 manage.py check

# 3. 啟動開發伺服器（使用 Python 3.11）
py -3.11 manage.py runserver
```

### 驗證所有依賴

```powershell
# 使用 Python 3.11 驗證
py -3.11 -c "import django; print('✅ Django:', django.get_version())"
py -3.11 -c "import firebase_admin; print('✅ Firebase: 已安裝')"
py -3.11 -c "import pymysql; print('✅ PyMySQL:', pymysql.__version__)"
```

## 已修復的問題

### 1. 遷移檔案錯誤

已修復 `myapp/migrations/0001_initial.py` 中的 `CheckConstraint` 語法錯誤：

**修復前**：
```python
models.CheckConstraint(condition=models.Q(('rating__gte', 1), ('rating__lte', 5)), name='rating_range')
```

**修復後**：
```python
models.CheckConstraint(check=models.Q(rating__gte=1, rating__lte=5), name='rating_range')
```

## 快速啟動腳本

創建一個批次檔來快速啟動專案：

```batch
@echo off
cd C:\CampingData
py -3.11 manage.py runserver
```

## 當前狀態總結

### ✅ 已完成

- [x] Python 3.11 已安裝
- [x] 所有依賴已安裝（Django 3.2.9, firebase-admin, PyMySQL）
- [x] Firebase 憑證檔案已放置
- [x] 遷移檔案已修復
- [x] 專案已遷移到 Firebase 分支

### ⚠️ 注意事項

- 需要使用 `py -3.11` 而不是 `python` 來運行專案
- 或調整 PATH 讓 Python 3.11 優先

## 下一步

1. **使用 Python 3.11 測試專案**：
   ```powershell
   py -3.11 manage.py check
   ```

2. **啟動開發伺服器**：
   ```powershell
   py -3.11 manage.py runserver
   ```

3. **訪問網站**：
   - 打開瀏覽器訪問：http://127.0.0.1:8000/

## 參考

- `修復遷移檔案錯誤.md` - 遷移檔案修復說明
- `安裝Python311完整指南.md` - Python 3.11 安裝指南

