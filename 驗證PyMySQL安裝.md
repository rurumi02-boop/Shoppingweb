# 驗證 PyMySQL 安裝

## 驗證方法

### 方法一：使用 Python 導入測試（最簡單）⭐

在 PowerShell 中執行：

```powershell
python -c "import pymysql; print('PyMySQL 安裝成功！版本：', pymysql.__version__)"
```

**成功輸出應該類似**：
```
PyMySQL 安裝成功！版本： 1.1.0
```

**如果失敗，會顯示**：
```
ModuleNotFoundError: No module named 'pymysql'
```

### 方法二：檢查 pip 已安裝套件列表

```powershell
pip list | findstr -i mysql
```

**成功輸出應該顯示**：
```
PyMySQL    1.1.0
```

### 方法三：查看詳細資訊

```powershell
pip show PyMySQL
```

**成功輸出會顯示**：
```
Name: PyMySQL
Version: 1.1.0
Summary: Pure Python MySQL Client
Home-page: https://github.com/PyMySQL/PyMySQL
...
```

### 方法四：在 Python 互動式環境中測試

```powershell
# 進入 Python 互動式環境
python

# 然後執行：
>>> import pymysql
>>> print(pymysql.__version__)
>>> exit()
```

**成功時不會有錯誤訊息**，會顯示版本號。

## 完整驗證腳本

您也可以執行以下完整驗證：

```powershell
# 1. 檢查是否在 pip 列表中
echo "檢查 pip 列表..."
pip list | findstr -i mysql

# 2. 嘗試導入模組
echo "`n嘗試導入 PyMySQL..."
python -c "import pymysql; print('✅ PyMySQL 安裝成功！版本：', pymysql.__version__)"

# 3. 查看詳細資訊
echo "`n查看詳細資訊..."
pip show PyMySQL
```

## 驗證結果說明

### ✅ 安裝成功

如果看到以下任何一種情況，表示安裝成功：
- `PyMySQL 安裝成功！版本： x.x.x`
- `pip list` 中顯示 `PyMySQL`
- `pip show PyMySQL` 顯示詳細資訊
- Python 可以成功 `import pymysql`

### ❌ 安裝失敗

如果看到以下錯誤，表示未安裝：
- `ModuleNotFoundError: No module named 'pymysql'`
- `pip list` 中沒有 `PyMySQL`
- `pip show PyMySQL` 顯示 `WARNING: Package(s) not found`

## 如果驗證失敗

### 重新安裝

```powershell
# 重新安裝 PyMySQL
pip install PyMySQL

# 或使用 --upgrade 強制更新
pip install --upgrade PyMySQL
```

### 檢查 Python 環境

```powershell
# 確認 Python 版本
python --version

# 確認 pip 版本
pip --version

# 確認 pip 指向正確的 Python
pip --version
python -m pip --version
```

### 使用完整路徑

如果有多個 Python 安裝：

```powershell
# 使用 python -m pip
python -m pip install PyMySQL
python -m pip list | findstr -i mysql
```

## 驗證所有依賴

同時驗證所有專案依賴：

```powershell
# 檢查所有已安裝的專案依賴
pip list | findstr -i "django firebase pymysql"

# 應該看到：
# Django      3.2.9
# firebase-admin  x.x.x
# PyMySQL     1.x.x
```

## 快速驗證命令

複製以下命令到 PowerShell 執行：

```powershell
python -c "import pymysql; print('✅ PyMySQL 安裝成功！版本：', pymysql.__version__)"
```

## 下一步

驗證成功後：
1. 如果使用 MySQL，在 `settings.py` 中添加：
   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   ```
2. 繼續 Firebase 設定（見 `FIREBASE_MIGRATION.md`）


