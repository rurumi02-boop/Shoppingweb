# 驗證 Django 安裝 - 完整指南

## 驗證方法

### 方法一：檢查 Django 版本（最簡單）⭐

在 PowerShell 中執行：

```powershell
python -c "import django; print('✅ Django 版本：', django.get_version())"
```

**成功輸出應該類似**：
```
✅ Django 版本： 3.2.9
```

**如果失敗，會顯示**：
```
ModuleNotFoundError: No module named 'django'
```

### 方法二：檢查 pip 已安裝套件列表

```powershell
pip list | findstr -i django
```

**成功輸出應該顯示**：
```
Django    3.2.9
```

### 方法三：查看詳細資訊

```powershell
pip show Django
```

**成功輸出會顯示**：
```
Name: Django
Version: 3.2.9
Summary: A high-level Python web framework
Home-page: https://www.djangoproject.com/
...
```

### 方法四：在 Python 互動式環境中測試

```powershell
# 進入 Python 互動式環境
python

# 然後執行：
>>> import django
>>> print(django.get_version())
>>> print(django.get_version())
3.2.9
>>> exit()
```

**成功時不會有錯誤訊息**，會顯示版本號。

### 方法五：使用 Django 管理命令

```powershell
# 檢查 Django 是否可用
python manage.py --version
```

**成功輸出應該顯示**：
```
3.2.9
```

## 完整驗證腳本

執行以下完整驗證：

```powershell
# 1. 檢查是否在 pip 列表中
echo "=== 檢查 pip 列表 ==="
pip list | findstr -i django

# 2. 嘗試導入模組並顯示版本
echo ""
echo "=== 檢查 Django 版本 ==="
python -c "import django; print('✅ Django 版本：', django.get_version())"

# 3. 查看詳細資訊
echo ""
echo "=== 查看詳細資訊 ==="
pip show Django

# 4. 使用 Django 管理命令
echo ""
echo "=== 使用 Django 管理命令 ==="
python manage.py --version
```

## 驗證結果說明

### ✅ 安裝成功

如果看到以下任何一種情況，表示安裝成功：
- `✅ Django 版本： 3.2.9`（或類似版本號）
- `pip list` 中顯示 `Django    3.2.9`
- `pip show Django` 顯示詳細資訊
- Python 可以成功 `import django`
- `python manage.py --version` 顯示版本號

### ❌ 安裝失敗

如果看到以下錯誤，表示未安裝：
- `ModuleNotFoundError: No module named 'django'`
- `pip list` 中沒有 `Django`
- `pip show Django` 顯示 `WARNING: Package(s) not found`
- `python manage.py --version` 顯示錯誤

## 如果驗證失敗（Django 未安裝）

### 安裝 Django

```powershell
# 安裝 Django 3.2.9（專案要求的版本）
pip install Django==3.2.9

# 或安裝所有專案依賴
pip install -r requirements.txt
```

### 驗證安裝

安裝完成後，再次執行驗證：

```powershell
python -c "import django; print('✅ Django 版本：', django.get_version())"
```

## 快速驗證命令

**最簡單的驗證方法**，複製以下命令到 PowerShell 執行：

```powershell
python -c "import django; print('✅ Django 版本：', django.get_version())"
```

## 同時驗證所有專案依賴

驗證 Django、Firebase 和 PyMySQL：

```powershell
echo "=== 驗證所有專案依賴 ==="
echo ""
python -c "import django; print('✅ Django:', django.get_version())"
python -c "import firebase_admin; print('✅ Firebase Admin SDK: 已安裝')"
python -c "import pymysql; print('✅ PyMySQL:', pymysql.__version__)"
echo ""
echo "=== 檢查 pip 列表 ==="
pip list | findstr -i "django firebase pymysql"
```

## 常見問題

### Q: Django 版本不是 3.2.9？
**A:** 
- 如果版本較新，通常沒問題
- 如果需要特定版本：`pip install Django==3.2.9`

### Q: 多個 Django 版本？
**A:** 
- 使用虛擬環境（推薦）
- 或使用 `python -m pip install Django==3.2.9` 確保安裝到正確的 Python

### Q: Django 已安裝但 `manage.py` 無法執行？
**A:** 
- 確認在專案根目錄（`C:\CampingData`）
- 確認 `manage.py` 文件存在
- 執行：`python manage.py --version`

## 下一步

驗證成功後：
1. 驗證 Firebase Admin SDK（見相關文件）
2. 設定 Firebase 憑證（見 `FIREBASE_MIGRATION.md`）
3. 執行資料庫遷移（如果需要）
4. 啟動開發伺服器：`python manage.py runserver`

## 參考

- `驗證PyMySQL安裝.md` - PyMySQL 驗證方法
- `FIREBASE_MIGRATION.md` - Firebase 遷移說明
- `requirements.txt` - 專案依賴列表


