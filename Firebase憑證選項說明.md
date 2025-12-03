# Firebase 憑證選項說明

## 您看到的選項

### 1. 「資料庫密鑰」(Database Secret) - 舊有憑證

**這是什麼**：
- 這是 Firebase Realtime Database 的舊版認證方式
- 用於直接存取 Firebase Realtime Database（不是 Firestore）
- **不適用於** Firebase Admin SDK

**何時使用**：
- 僅在使用 Firebase Realtime Database 的舊專案
- 不適用於 Firestore 或 Admin SDK

**建議**：❌ **不要選擇這個**，因為您的專案使用 Firestore 和 Admin SDK

---

### 2. 「所有服務帳戶」(All Service Accounts) - 5 個服務帳戶

**這是什麼**：
- 顯示專案中所有的服務帳戶
- 服務帳戶是應用程式用來存取 Firebase 服務的帳號
- 每個服務帳戶都有自己的私密金鑰

**何時使用**：
- 查看和管理所有服務帳戶
- 創建新的服務帳戶
- 管理現有服務帳戶的權限

**建議**：✅ **可以點擊查看**，但主要操作在下方

---

### 3. 「Firebase 服務帳戶」- 主要選項 ⭐

**這是什麼**：
- Firebase 專案預設的服務帳戶
- 用於 Firebase Admin SDK
- 這是您需要的選項！

**服務帳戶 Email**：
```
firebase-adminsdk-fbsvc@campingdata-1ebb6.iam.gserviceaccount.com
```

**建議**：✅ **使用這個服務帳戶**

---

## 您應該做什麼

### 步驟 1：選擇 Python 語言

在「Admin SDK 設定程式碼片段」區域：
1. 點擊 **「Python」** 選項（目前顯示的是 Node.js）
2. 這樣會顯示 Python 的設定範例

### 步驟 2：產生新的私密金鑰

1. 找到藍色的按鈕：**「產生新的私密金鑰」**
2. 點擊這個按鈕
3. 系統會下載一個 JSON 檔案

### 步驟 3：儲存憑證檔案

1. 將下載的 JSON 檔案重命名為：`firebase-credentials.json`
2. 放在專案根目錄：`C:\CampingData\firebase-credentials.json`

---

## 詳細步驟指南

### 完整操作流程

1. **在 Firebase Console 中**：
   - 確認您在「專案設定」頁面
   - 確認看到「Firebase 服務帳戶」區塊

2. **選擇 Python**：
   - 在「Admin SDK 設定程式碼片段」中
   - 點擊 **「Python」** 選項（不是 Node.js）

3. **產生私密金鑰**：
   - 點擊藍色按鈕：**「產生新的私密金鑰」**
   - 系統會提示下載 JSON 檔案
   - 點擊「下載」或「儲存」

4. **處理下載的檔案**：
   - 找到下載的 JSON 檔案（通常在「下載」資料夾）
   - 檔案名稱類似：`campingdata-1ebb6-firebase-adminsdk-xxxxx.json`
   - 將它複製到專案目錄：`C:\CampingData\`
   - 重命名為：`firebase-credentials.json`

5. **驗證檔案位置**：
   ```powershell
   # 在 PowerShell 中執行
   cd C:\CampingData
   dir firebase-credentials.json
   ```
   應該顯示檔案存在

---

## 各選項的用途對照表

| 選項 | 用途 | 適用於您的專案？ |
|------|------|----------------|
| 資料庫密鑰 | Firebase Realtime Database（舊版） | ❌ 不適用 |
| 所有服務帳戶 | 管理服務帳戶列表 | ⚠️ 可查看，但不是主要操作 |
| Firebase 服務帳戶 | Firebase Admin SDK（Firestore） | ✅ **使用這個** |

---

## 重要提醒

### ⚠️ 安全注意事項

1. **不要提交到 Git**：
   - `firebase-credentials.json` 包含敏感資訊
   - 已在 `.gitignore` 中排除
   - 不要分享或上傳這個檔案

2. **檔案內容**：
   - JSON 檔案包含私密金鑰
   - 可以存取您的 Firebase 專案
   - 請妥善保管

3. **如果遺失**：
   - 可以重新產生新的私密金鑰
   - 舊的金鑰會失效
   - 建議定期輪換

---

## 驗證設定

放置憑證檔案後，驗證設定：

```powershell
# 在 PowerShell 中執行
cd C:\CampingData

# 檢查檔案是否存在
dir firebase-credentials.json

# 測試 Django 專案（應該不會再顯示 Firebase 警告）
python manage.py check
```

---

## 常見問題

### Q: 應該選擇「資料庫密鑰」還是「服務帳戶」？
**A:** 選擇「服務帳戶」並產生私密金鑰。資料庫密鑰是舊版，不適用於 Firestore。

### Q: 有 5 個服務帳戶，應該用哪一個？
**A:** 使用預設的「Firebase 服務帳戶」（firebase-adminsdk-fbsvc@...），這是專案自動創建的。

### Q: 可以創建新的服務帳戶嗎？
**A:** 可以，但通常不需要。使用預設的 Firebase 服務帳戶即可。

### Q: 私密金鑰檔案名稱很重要嗎？
**A:** 檔案名稱可以自訂，但建議使用 `firebase-credentials.json`，這樣 `settings.py` 中的設定才能正確找到。

---

## 下一步

完成憑證設定後：
1. 驗證檔案已正確放置
2. 測試 Django 專案：`python manage.py check`
3. 啟動開發伺服器：`python manage.py runserver`
4. 測試 Firebase 功能

