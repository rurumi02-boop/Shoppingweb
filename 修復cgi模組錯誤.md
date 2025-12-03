# 修復 ModuleNotFoundError: No module named 'cgi'

## 問題說明

**錯誤**：`ModuleNotFoundError: No module named 'cgi'`

**原因**：
- Python 3.14.0 移除了 `cgi` 模組
- Django 3.2.9 仍在使用 `cgi` 模組
- 這是版本不相容問題

## 解決方案

### 方案一：降級到 Python 3.11（推薦）⭐

**最穩定且推薦的解決方案**

#### 步驟：

1. **下載 Python 3.11**
   - 前往：https://www.python.org/downloads/release/python-3110/
   - 下載：**Windows installer (64-bit)**
   - 檔案名稱類似：`python-3.11.0-amd64.exe`

2. **安裝 Python 3.11**
   - 執行安裝程式
   - ⚠️ **重要**：勾選「**Add Python to PATH**」
   - 選擇「Install Now」或「Customize installation」
   - 等待安裝完成

3. **重新開啟 PowerShell**
   - 關閉當前 PowerShell 視窗
   - 開啟新的 PowerShell 視窗

4. **驗證 Python 版本**
   ```powershell
   python --version
   # 應該顯示：Python 3.11.0（或類似）
   ```

5. **重新安裝依賴**
   ```powershell
   cd C:\CampingData
   pip install -r requirements.txt
   ```

6. **測試 Django**
   ```powershell
   python manage.py check
   ```

### 方案二：升級 Django 版本

升級到支援 Python 3.14 的 Django 版本。

#### 步驟：

1. **升級 Django**
   ```powershell
   pip install --upgrade Django
   ```

2. **測試**
   ```powershell
   python manage.py check
   ```

3. **注意**：
   - Django 4.2+ 支援 Python 3.8-3.11
   - Python 3.14 可能需要 Django 5.0+（如果已發布）
   - 升級後可能需要修改部分程式碼

### 方案三：使用 Python Launcher 指定版本

如果系統中同時安裝了多個 Python 版本：

```powershell
# 使用 Python 3.11（如果已安裝）
py -3.11 manage.py check

# 或指定完整路徑
C:\Python311\python.exe manage.py check
```

### 方案四：手動修復 Django（臨時方案，不推薦）

可以手動修復 Django 3.2.9 的 `cgi` 導入問題，但這不是長期解決方案。

## 推薦做法

### 使用 Python 3.11（最穩定）

**為什麼選擇 Python 3.11**：
- ✅ Django 3.2.9 官方支援 Python 3.6-3.10，Python 3.11 測試通過
- ✅ 穩定且成熟
- ✅ 與 Django 3.2.9 完全相容
- ✅ 效能良好

**安裝步驟**：

1. **下載 Python 3.11.0**
   ```
   https://www.python.org/downloads/release/python-3110/
   ```

2. **安裝時務必勾選「Add Python to PATH」**

3. **重新開啟 PowerShell 後驗證**：
   ```powershell
   python --version
   ```

4. **重新安裝依賴**：
   ```powershell
   cd C:\CampingData
   pip install -r requirements.txt
   ```

5. **測試**：
   ```powershell
   python manage.py check
   ```

## 版本相容性參考

| Python 版本 | Django 3.2.9 支援 | 狀態 |
|------------|------------------|------|
| Python 3.8 | ✅ 官方支援 | 推薦 |
| Python 3.9 | ✅ 官方支援 | 推薦 |
| Python 3.10 | ✅ 官方支援 | 推薦 |
| Python 3.11 | ⚠️ 測試通過 | 可用 |
| Python 3.12 | ❌ 未測試 | 可能可用 |
| Python 3.13 | ❌ 未測試 | 可能可用 |
| Python 3.14 | ❌ 不相容 | **不支援** |

## 快速檢查

安裝 Python 3.11 後，執行：

```powershell
# 1. 檢查 Python 版本
python --version
# 應該顯示：Python 3.11.x

# 2. 檢查 pip
pip --version

# 3. 重新安裝依賴
cd C:\CampingData
pip install -r requirements.txt

# 4. 測試 Django
python manage.py check
# 應該沒有錯誤

# 5. 測試 Firebase
python -c "from firebase_admin import firestore; db = firestore.client(); print('✅ Firebase 連接成功')"
```

## 如果不想降級 Python

### 選項 1：升級 Django

```powershell
# 升級到最新版本
pip install --upgrade Django

# 測試
python manage.py check
```

**注意**：升級 Django 可能需要修改部分程式碼。

### 選項 2：等待 Django 更新

等待 Django 發布支援 Python 3.14 的版本。

## 當前狀態

### ✅ 已完成
- Firebase 憑證檔案已正確放置
- Firebase Admin SDK 可以正常導入
- 所有依賴套件已安裝

### ❌ 待解決
- Python 3.14 與 Django 3.2.9 相容性問題

## 建議

**強烈建議安裝 Python 3.11**，因為：
1. 與 Django 3.2.9 完全相容
2. 穩定可靠
3. 不需要修改程式碼
4. 是最快的解決方案

## 安裝完成後

安裝 Python 3.11 並重新安裝依賴後，專案應該可以正常運行：

```powershell
# 啟動開發伺服器
python manage.py runserver

# 訪問 http://127.0.0.1:8000/
```

