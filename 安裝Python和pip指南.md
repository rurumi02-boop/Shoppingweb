# Python 和 pip 安裝指南

## 錯誤說明

當您看到以下錯誤：
```
'pip' is not recognized as an internal or external command,
operable program or batch file.
```

這表示：
- Python 可能未安裝
- 或 Python 已安裝但 pip 不在系統 PATH 環境變數中

## 解決方案

### 方法一：安裝 Python（如果尚未安裝）

1. **下載 Python**
   - 前往：https://www.python.org/downloads/
   - 下載最新版本的 Python（建議 Python 3.11 或 3.12）

2. **安裝 Python**
   - 執行下載的安裝程式
   - ⚠️ **重要**：勾選「**Add Python to PATH**」（將 Python 加入 PATH）
   - 點擊「Install Now」
   - 等待安裝完成

3. **驗證安裝**
   - 關閉並重新開啟命令提示字元
   - 執行：`python --version`
   - 執行：`pip --version`
   - 如果顯示版本號，表示安裝成功

### 方法二：使用 python -m pip（如果 Python 已安裝）

如果 Python 已安裝但 pip 命令無法使用，可以嘗試：

```bash
# 使用 python -m pip 代替 pip
python -m pip install -r requirements.txt

# 或使用 py 啟動器（Windows）
py -m pip install -r requirements.txt
```

### 方法三：檢查 Python 安裝位置

1. **找到 Python 安裝位置**
   - 通常在：`C:\Users\您的使用者名稱\AppData\Local\Programs\Python\`
   - 或：`C:\Program Files\Python3x\`

2. **手動加入 PATH**
   - 右鍵「此電腦」→「內容」→「進階系統設定」
   - 點擊「環境變數」
   - 在「系統變數」中找到「Path」，點擊「編輯」
   - 新增 Python 安裝路徑（例如：`C:\Python311`）
   - 新增 Scripts 資料夾（例如：`C:\Python311\Scripts`）
   - 確定並重新開啟命令提示字元

## 安裝 Firebase 依賴

安裝 Python 後，在專案目錄執行：

```bash
# 方法 1：直接使用 pip
pip install -r requirements.txt

# 方法 2：使用 python -m pip
python -m pip install -r requirements.txt

# 方法 3：使用 py 啟動器（Windows）
py -m pip install -r requirements.txt
```

## 驗證安裝

安裝完成後，驗證 Firebase Admin SDK 是否已安裝：

```bash
python -c "import firebase_admin; print('Firebase Admin SDK 已安裝')"
```

## 常見問題

### Q: 安裝 Python 時忘記勾選 "Add Python to PATH"
**A:** 
1. 重新執行 Python 安裝程式
2. 選擇「Modify」（修改）
3. 勾選「Add Python to PATH」
4. 或手動加入 PATH（見方法三）

### Q: 多個 Python 版本
**A:** 
- 使用 `py` 啟動器指定版本：`py -3.11 -m pip install -r requirements.txt`
- 或使用完整路徑：`C:\Python311\python.exe -m pip install -r requirements.txt`

### Q: 權限問題
**A:** 
- 以系統管理員身分執行命令提示字元
- 或使用 `--user` 參數：`pip install --user -r requirements.txt`

## 快速檢查清單

- [ ] Python 已安裝
- [ ] 安裝時勾選了 "Add Python to PATH"
- [ ] 已重新開啟命令提示字元
- [ ] `python --version` 可以執行
- [ ] `pip --version` 或 `python -m pip --version` 可以執行

## 需要幫助？

如果仍有問題，請告訴我：
1. 您是否已安裝 Python？
2. 執行 `python --version` 的結果是什麼？
3. 執行 `python -m pip --version` 的結果是什麼？


