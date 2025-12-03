# 放置 Firebase 憑證檔案指南

## 當前狀況

您已經下載了 Firebase 憑證檔案，但檔案還沒有放在專案目錄中。

## 步驟 1：找到下載的檔案

### 方法一：檢查下載資料夾

1. **開啟檔案總管**
2. **前往下載資料夾**：
   - 通常位置：`C:\Users\您的使用者名稱\Downloads`
   - 或按 `Win + R`，輸入 `%USERPROFILE%\Downloads`

3. **尋找 JSON 檔案**：
   - 檔案名稱類似：`campingdata-1ebb6-firebase-adminsdk-xxxxx.json`
   - 或包含：`firebase`、`adminsdk`、`campingdata` 等關鍵字
   - 檔案類型：JSON 檔案
   - 最近下載的檔案（按日期排序）

### 方法二：使用 PowerShell 尋找

在 PowerShell 中執行：

```powershell
# 尋找下載資料夾中的 Firebase 相關檔案
Get-ChildItem "$env:USERPROFILE\Downloads" -Filter "*.json" | 
    Where-Object { $_.Name -like "*firebase*" -or $_.Name -like "*campingdata*" -or $_.Name -like "*adminsdk*" } | 
    Select-Object Name, FullName, LastWriteTime | 
    Sort-Object LastWriteTime -Descending
```

這會顯示所有可能的 Firebase 憑證檔案。

## 步驟 2：複製檔案到專案目錄

### 方法一：使用檔案總管（最簡單）

1. **找到下載的 JSON 檔案**
2. **右鍵點擊檔案** → 選擇「複製」
3. **前往專案目錄**：`C:\CampingData`
4. **在專案目錄中右鍵** → 選擇「貼上」

### 方法二：使用 PowerShell

如果找到檔案，執行：

```powershell
# 假設檔案名稱是 campingdata-1ebb6-firebase-adminsdk-xxxxx.json
# 請替換為實際的檔案名稱

# 複製檔案到專案目錄
Copy-Item "$env:USERPROFILE\Downloads\campingdata-1ebb6-firebase-adminsdk-xxxxx.json" -Destination "C:\CampingData\firebase-credentials.json"
```

## 步驟 3：重命名檔案

### 方法一：在檔案總管中重命名

1. **在 `C:\CampingData` 目錄中**
2. **找到剛才複製的 JSON 檔案**
3. **右鍵點擊檔案** → 選擇「重新命名」
4. **輸入新名稱**：`firebase-credentials.json`
5. **按 Enter 確認**

### 方法二：使用 PowerShell

如果檔案已經在專案目錄中，執行：

```powershell
cd C:\CampingData

# 重命名檔案（請替換為實際的檔案名稱）
Rename-Item "campingdata-1ebb6-firebase-adminsdk-xxxxx.json" -NewName "firebase-credentials.json"
```

## 完整操作流程（使用 PowerShell）

如果已經找到檔案，可以一次完成：

```powershell
# 1. 切換到專案目錄
cd C:\CampingData

# 2. 找到下載的檔案（請替換為實際的檔案名稱）
$sourceFile = "$env:USERPROFILE\Downloads\campingdata-1ebb6-firebase-adminsdk-xxxxx.json"

# 3. 複製並重命名
Copy-Item $sourceFile -Destination "C:\CampingData\firebase-credentials.json"

# 4. 驗證
dir firebase-credentials.json
```

## 驗證檔案位置

完成後，在 PowerShell 中執行：

```powershell
cd C:\CampingData

# 檢查檔案是否存在
dir firebase-credentials.json

# 應該顯示檔案資訊，例如：
#    目錄: C:\CampingData
#    Mode                 LastWriteTime         Length Name
#    ----                 -------------         ------ ----
#    -a----        2024/xx/xx     xx:xx         xxxx firebase-credentials.json
```

## 如果找不到下載的檔案

### 檢查其他可能的位置

```powershell
# 檢查桌面
Get-ChildItem "$env:USERPROFILE\Desktop" -Filter "*.json" -ErrorAction SilentlyContinue

# 檢查文件資料夾
Get-ChildItem "$env:USERPROFILE\Documents" -Filter "*.json" -ErrorAction SilentlyContinue

# 搜尋整個使用者目錄（較慢）
Get-ChildItem "$env:USERPROFILE" -Filter "*firebase*.json" -Recurse -ErrorAction SilentlyContinue | Select-Object FullName
```

### 重新下載

如果找不到檔案，可以：
1. 回到 Firebase Console
2. 再次點擊「產生新的私密金鑰」
3. 注意下載位置
4. 立即複製到專案目錄

## 檔案內容確認

檔案應該是 JSON 格式，包含類似以下內容：

```json
{
  "type": "service_account",
  "project_id": "campingdata-1ebb6",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@campingdata-1ebb6.iam.gserviceaccount.com",
  ...
}
```

## 測試設定

放置檔案後，測試 Django 專案：

```powershell
cd C:\CampingData

# 測試 Django（應該不會再顯示 Firebase 警告）
python manage.py check
```

如果成功，應該不會再看到 Firebase 憑證檔案未找到的警告。

## 常見問題

### Q: 檔案名稱很長，可以重命名嗎？
**A:** 可以，必須重命名為 `firebase-credentials.json`

### Q: 可以放在其他位置嗎？
**A:** 可以，但需要修改 `settings.py` 中的路徑設定。建議放在專案根目錄。

### Q: 檔案內容看起來是亂碼？
**A:** 這是正常的，JSON 檔案中的私密金鑰是加密的格式。

## 下一步

完成後：
1. 驗證檔案已正確放置
2. 測試 Django 專案
3. 啟動開發伺服器：`python manage.py runserver`

