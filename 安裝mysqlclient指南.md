# 安裝 mysqlclient 指南

## ✅ 已取消註解

`requirements.txt` 中的 `mysqlclient` 行已取消註解，現在可以安裝了。

## 安裝步驟

### 方法一：安裝所有依賴（推薦）

在新的 PowerShell 視窗中執行：

```powershell
# 確保在專案目錄
cd C:\CampingData

# 安裝所有依賴（包括 mysqlclient）
pip install -r requirements.txt
```

### 方法二：單獨安裝 mysqlclient

如果只想安裝 mysqlclient：

```powershell
pip install mysqlclient
```

## 驗證安裝

安裝完成後，驗證 mysqlclient 是否成功安裝：

```powershell
# 檢查已安裝的套件
pip list | findstr mysqlclient

# 或使用 Python 驗證
python -c "import MySQLdb; print('mysqlclient 安裝成功！')"
```

## 如果安裝成功

您應該看到：
- `mysqlclient` 出現在 `pip list` 中
- Python 可以成功導入 `MySQLdb` 模組

## 如果仍有錯誤

### 錯誤 1：仍需要 C++ Build Tools

如果還是出現 C++ 編譯器錯誤：

1. **確認 C++ Build Tools 已正確安裝**
   - 開啟「Visual Studio Installer」
   - 確認「C++ build tools」工作負載已安裝

2. **重新啟動電腦**（建議）
   - 安裝 C++ Build Tools 後，可能需要重新啟動才能生效

3. **確認環境變數**
   - 確保 Visual Studio 的編譯器在 PATH 中

### 錯誤 2：找不到 MySQL 開發庫

如果出現 MySQL 相關錯誤，可能需要：

1. **安裝 MySQL Connector/C**
   - 下載：https://dev.mysql.com/downloads/connector/c/
   - 安裝後，mysqlclient 才能找到 MySQL 開發庫

2. **或使用 PyMySQL 替代**（純 Python 實現，不需要編譯）
   ```powershell
   pip install PyMySQL
   ```
   然後在 `settings.py` 中添加：
   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

## 當前 requirements.txt 內容

```txt
Django==3.2.9
firebase-admin>=6.0.0
mysqlclient>=2.1.0
```

## 使用場景

現在您的專案可以：
- ✅ 使用 Firebase Firestore（主要資料庫）
- ✅ 使用 MySQL（如果需要）
- ✅ 同時支援兩種資料庫

## 下一步

1. **安裝依賴**：`pip install -r requirements.txt`
2. **驗證安裝**：確認所有套件都安裝成功
3. **設定資料庫**：
   - Firebase：設定 `firebase-credentials.json`
   - MySQL：在 `settings.py` 中配置（如果需要）

## 注意事項

- 如果主要使用 Firebase，mysqlclient 不會影響 Firebase 功能
- mysqlclient 只有在使用 MySQL 時才會被調用
- 兩個資料庫可以共存，根據需求選擇使用


