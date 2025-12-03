# 解決 mysqlclient 安裝錯誤

## 錯誤說明

錯誤訊息：
```
error: Microsoft Visual C++ 14.0 or greater is required.
Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
ERROR: Failed building wheel for mysqlclient
```

**原因**：`mysqlclient` 是一個需要編譯的 Python 套件，需要 C++ 編譯器才能安裝。

## 解決方案

### ⚠️ 重要：您正在使用 Firebase 分支

由於您已經遷移到 Firebase 分支，**可能不需要 `mysqlclient`**（因為資料庫已改用 Firebase）。

### 方案一：移除 mysqlclient（推薦，如果使用 Firebase）

如果您的專案已經改用 Firebase，可以從 `requirements.txt` 中移除 `mysqlclient`：

1. **編輯 requirements.txt**，移除或註解 `mysqlclient` 這一行：
   ```txt
   Django==3.2.9
   firebase-admin>=6.0.0
   # mysqlclient>=2.1.0  # 已改用 Firebase，不需要 MySQL
   ```

2. **重新安裝依賴**：
   ```powershell
   pip install -r requirements.txt
   ```

### 方案二：安裝 Microsoft C++ Build Tools（如果需要保留 MySQL 支援）

如果您需要同時支援 MySQL 和 Firebase，可以安裝編譯工具：

1. **下載 Microsoft C++ Build Tools**
   - 前往：https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - 下載「Build Tools for Visual Studio」

2. **安裝步驟**
   - 執行安裝程式
   - 選擇「C++ build tools」工作負載
   - 點擊「安裝」
   - 等待安裝完成（可能需要幾分鐘到幾十分鐘）

3. **重新安裝 mysqlclient**
   ```powershell
   pip install mysqlclient
   ```

### 方案三：使用預編譯的 wheel 文件

嘗試使用預編譯的版本（如果可用）：

```powershell
# 嘗試安裝特定版本
pip install mysqlclient==2.1.1

# 或使用 conda（如果已安裝）
conda install -c conda-forge mysqlclient
```

### 方案四：使用 PyMySQL（替代方案）

如果不需要 `mysqlclient` 的完整功能，可以使用純 Python 實現的 `PyMySQL`：

1. **修改 requirements.txt**：
   ```txt
   Django==3.2.9
   firebase-admin>=6.0.0
   PyMySQL>=1.0.0
   ```

2. **在 settings.py 中添加**（如果使用 MySQL）：
   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

## 推薦做法

### 如果您使用 Firebase 分支：

**直接移除 mysqlclient**，因為：
- 資料庫已改用 Firebase Firestore
- 不需要 MySQL 連接器
- 可以避免編譯問題

**步驟**：
1. 編輯 `requirements.txt`，註解或刪除 `mysqlclient>=2.1.0`
2. 重新執行：`pip install -r requirements.txt`

### 如果您需要同時支援 MySQL 和 Firebase：

安裝 Microsoft C++ Build Tools（方案二）

## 驗證安裝

安裝完成後（移除 mysqlclient 或安裝編譯工具後），驗證：

```powershell
# 檢查已安裝的套件
pip list

# 應該看到：
# - Django 3.2.9
# - firebase-admin
# - （如果保留）mysqlclient 或 PyMySQL
```

## 下一步

1. **選擇解決方案**（推薦：移除 mysqlclient）
2. **重新安裝依賴**：`pip install -r requirements.txt`
3. **驗證安裝**：`pip list`
4. **繼續 Firebase 設定**（見 `FIREBASE_MIGRATION.md`）


