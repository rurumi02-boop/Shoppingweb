# 解決 Python 3.14 與 Django 3.2.9 相容性問題

## 問題說明

錯誤訊息：
```
ModuleNotFoundError: No module named 'cgi'
```

**原因**：
- Python 3.14.0 移除了 `cgi` 模組
- Django 3.2.9 仍在使用 `cgi` 模組
- 這是版本不相容的問題

## 解決方案

### 方案一：降級 Python 版本（推薦）⭐

Django 3.2.9 建議使用 Python 3.8-3.11。

#### 步驟：

1. **安裝 Python 3.11**（推薦版本）
   - 下載：https://www.python.org/downloads/release/python-3110/
   - 選擇 Windows installer (64-bit)
   - 安裝時勾選「Add Python to PATH」

2. **驗證安裝**
   ```powershell
   python --version
   # 應該顯示：Python 3.11.x
   ```

3. **重新安裝依賴**
   ```powershell
   cd C:\CampingData
   pip install -r requirements.txt
   ```

4. **測試 Django**
   ```powershell
   python manage.py check
   ```

### 方案二：升級 Django 版本

升級到支援 Python 3.14 的 Django 版本（需要測試相容性）。

#### 步驟：

1. **升級 Django**
   ```powershell
   pip install --upgrade Django
   ```

2. **測試相容性**
   ```powershell
   python manage.py check
   ```

3. **注意**：可能需要修改部分程式碼以適應新版本

### 方案三：使用 Python Launcher 指定版本

如果系統中有多個 Python 版本：

```powershell
# 使用 Python 3.11（如果已安裝）
py -3.11 manage.py check
```

## 推薦做法

### 使用 Python 3.11（最穩定）

1. **下載 Python 3.11**
   - 前往：https://www.python.org/downloads/release/python-3110/
   - 下載：Windows installer (64-bit)

2. **安裝時注意**
   - 勾選「Add Python to PATH」
   - 可以選擇「Install for all users」（可選）

3. **重新開啟 PowerShell**

4. **驗證版本**
   ```powershell
   python --version
   # 應該顯示：Python 3.11.x
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

## 當前狀態

### ✅ 已完成

- [x] Firebase 憑證檔案已正確放置
- [x] Firebase Admin SDK 可以正常導入
- [x] 所有依賴套件已安裝

### ❌ 待解決

- [ ] Python 3.14 與 Django 3.2.9 相容性問題

## 版本相容性參考

| Django 版本 | Python 版本支援 |
|------------|----------------|
| Django 3.2 | Python 3.6-3.10（官方）<br>Python 3.11（測試） |
| Django 4.0+ | Python 3.8+ |
| Django 4.2+ | Python 3.8-3.11 |

**Python 3.14** 是較新的版本，Django 3.2.9 可能尚未完全支援。

## 快速解決

**最簡單的方法**：安裝 Python 3.11

1. 下載：https://www.python.org/downloads/release/python-3110/
2. 安裝（勾選 Add to PATH）
3. 重新開啟 PowerShell
4. 執行：`pip install -r requirements.txt`
5. 測試：`python manage.py check`

## 驗證

解決後，應該可以：

```powershell
# 檢查 Python 版本
python --version
# 應該顯示：Python 3.11.x

# 測試 Django
python manage.py check
# 應該沒有錯誤

# 測試 Firebase
python -c "from firebase_admin import firestore; db = firestore.client(); print('✅ Firebase 連接成功')"
```

