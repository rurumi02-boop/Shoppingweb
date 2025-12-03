# Firebase 遷移說明

## 概述

此專案已**完全遷移到 Firebase Firestore**，不再使用 MySQL 或其他傳統資料庫。所有資料操作都通過 Firebase 服務層進行。

## ✅ 遷移狀態

- ✅ **資料庫**: 100% 使用 Firebase Firestore
- ✅ **MySQL**: 已完全移除，不再需要
- ✅ **PyMySQL**: 已移除，不再需要
- ✅ **所有功能**: 已遷移到 Firebase

## 已完成的變更

### 1. 新增檔案
- `myapp/firebase_service.py` - Firebase 服務層，封裝所有資料庫操作
- `FIREBASE_MIGRATION.md` - 本說明文件
- `完全使用Firebase設定完成.md` - 完整遷移記錄

### 2. 修改的檔案
- `CampingData/settings.py` - 添加 Firebase 初始化，移除所有 MySQL 設定
- `CampingData/__init__.py` - 移除 PyMySQL 導入
- `myapp/views.py` - 所有資料庫操作改為使用 Firebase 服務層
- `requirements.txt` - 移除 PyMySQL 和 mysqlclient 依賴
- `.gitignore` - 確保 Firebase 憑證不被提交
- `README.md` - 更新為 Firebase 說明

## 安裝與設定

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

**必要套件**:
- `Django==3.2.9`
- `firebase-admin>=6.0.0`

**不再需要**:
- ❌ `PyMySQL` - 已移除
- ❌ `mysqlclient` - 已移除
- ❌ MySQL 資料庫 - 不需要

### 2. 取得 Firebase 憑證

1. 前往 [Firebase Console](https://console.firebase.google.com/)
2. 創建或選擇專案
3. 前往「專案設定」→「服務帳號」
4. 點擊「產生新的私密金鑰」
5. 下載 JSON 檔案並重命名為 `firebase-credentials.json`
6. 將檔案放在專案根目錄（`C:\CampingData\firebase-credentials.json`）

### 3. 設定 Firebase

確保 `firebase-credentials.json` 在專案根目錄，Django 啟動時會自動初始化 Firebase。

**驗證設定**:
```powershell
# 檢查憑證檔案是否存在
Test-Path C:\CampingData\firebase-credentials.json
```

應該回傳 `True`

## 架構變更

### 資料庫操作
- **原本**：使用 Django ORM (`Product.objects.filter()`, `Category.objects.all()` 等)
- **現在**：使用 Firebase 服務層 (`FirebaseService.get_products()`, `FirebaseService.get_all_categories()` 等)

### 使用者認證
- **保留**：Django 的 User 模型和認證系統（用於登入/登出）
- **新增**：在 Firebase 中同步使用者資料（用於資料查詢）

### 資料結構

Firebase 使用集合（Collections）和文件（Documents）：

- `users` - 使用者資料
- `products` - 商品資料
- `categories` - 分類資料
- `brands` - 品牌資料
- `orders` - 訂單資料
- `order_items` - 訂單項目
- `wishlist` - 我的最愛
- `reviews` - 商品評論

## 已修改的功能

### ✅ 已遷移的功能

1. **首頁** (`home()`) - 顯示分類商品
2. **新商品** (`new_products()`) - 顯示最近 30 天的新商品
3. **商品列表** (`ProductListView`) - 支援分類、品牌、關鍵字搜尋
4. **商品詳情** (`ProductDetailView`) - 顯示商品詳細資訊（包含評等、評價、變體選擇等）
5. **使用者註冊** (`register()`) - 同時在 Django 和 Firebase 創建使用者
6. **使用者資訊** (`user_info()`) - 顯示訂單和我的最愛
7. **購物車** (`add_to_cart()`) - 使用 Firebase 取得商品資訊
8. **訂單提交** (`submit_order()`) - 在 Firebase 創建訂單
9. **我的最愛** (`toggle_wishlist()`) - 使用 Firebase 管理
10. **商品編輯器** (`product_editor()`, `submit_product_add()`) - 使用 Firebase 管理商品
11. **直接購買** (`buy_now()`) - 直接購買功能
12. **商品評價** - 顯示和創建商品評價

### ⚠️ 注意事項

- **使用者認證**：仍使用 Django 的認證系統，但使用者資料會同步到 Firebase
- **分頁**：`ProductListView` 已改為手動分頁（Firebase 不支援 Django 的內建分頁）
- **搜尋**：關鍵字搜尋改為在記憶體中過濾（Firebase 不支援全文搜尋）
- **Django 遷移**：不需要執行 `python manage.py migrate`（針對資料模型）

## 資料庫設定

### settings.py 設定

```python
# 此專案完全使用 Firebase Firestore 作為資料庫
# 不使用 MySQL 或其他傳統資料庫
# 所有資料操作都通過 myapp/firebase_service.py 中的 Firebase 服務層進行

# Django 的 DATABASES 設定僅作為佔位用，避免 Django 框架錯誤
# 實際上所有資料都儲存在 Firebase Firestore 中
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_firebase_placeholder.sqlite3',  # 佔位用，不會實際使用
    }
}
```

### Firebase 初始化

Firebase 在 `settings.py` 中自動初始化：

```python
# Firebase 初始化（需要服務帳號金鑰檔案）
FIREBASE_CREDENTIALS_PATH = BASE_DIR / 'firebase-credentials.json'

if not firebase_admin._apps:
    if FIREBASE_CREDENTIALS_PATH.exists():
        cred = credentials.Certificate(str(FIREBASE_CREDENTIALS_PATH))
        firebase_admin.initialize_app(cred)
    else:
        print("⚠️  警告：未找到 Firebase 憑證檔案")
```

## 資料遷移

### 從 MySQL 遷移到 Firebase

如果需要從現有的 MySQL 資料庫遷移資料，可以建立遷移腳本：

**範例遷移腳本**（需要時可建立）：
```python
# migrate_data_to_firebase.py
from myapp.firebase_service import FirebaseService

def migrate_products():
    # 從 MySQL 讀取資料（如果還有 MySQL 連線）
    # products = Product.objects.all()
    
    # 寫入 Firebase
    for product in products:
        FirebaseService.create_product({
            'product_name': product.product_name,
            'description': product.description,
            'price': product.price,
            # ... 其他欄位
        })
```

## 測試

### 測試步驟

1. **確認 Firebase 憑證**
   ```powershell
   Test-Path C:\CampingData\firebase-credentials.json
   ```

2. **啟動 Django 開發伺服器**
   ```bash
   py -3.11 manage.py runserver
   ```

3. **測試各個功能**：
   - 瀏覽首頁：http://127.0.0.1:8000/
   - 查看商品列表：http://127.0.0.1:8000/products/
   - 查看商品詳情：點擊任一商品
   - 註冊新使用者：http://127.0.0.1:8000/register/
   - 加入購物車：在商品詳情頁點擊「加入購物車」
   - 提交訂單：完成購物流程
   - 測試我的最愛：收藏/取消收藏商品

詳細測試步驟請參考：`網頁功能測試步驟指南.md`

## 已知限制

1. **全文搜尋**：Firebase 不支援全文搜尋，關鍵字搜尋改為在記憶體中過濾
2. **複雜查詢**：Firebase 查詢功能較受限，需要調整查詢邏輯
3. **交易**：Firebase 交易語意不同，需要重新設計
4. **分頁**：需要手動實作分頁功能
5. **Django Admin**：Django Admin 無法直接管理 Firebase 資料（需要使用 Firebase Console）

## 常見問題

### Q: 為什麼還需要 SQLite 佔位資料庫？

A: Django 框架要求必須有 DATABASES 設定，即使不使用。SQLite 佔位資料庫只是為了避免 Django 錯誤，實際上不會被使用。

### Q: 看到遷移警告怎麼辦？

A: 這是正常的。因為專案使用 Firebase，不依賴 Django 的遷移系統，可以安全忽略這些警告。

### Q: 如何查看 Firebase 中的資料？

A: 前往 [Firebase Console](https://console.firebase.google.com/)，選擇專案，進入 Firestore Database 即可查看所有資料。

### Q: 如何備份資料？

A: 使用 Firebase Console 的匯出功能，或使用 Firebase Admin SDK 的匯出 API。

## 後續工作

- [x] 完全移除 MySQL 相關設定
- [x] 移除 PyMySQL 依賴
- [x] 更新所有文件
- [ ] 建立資料遷移腳本（如需要）
- [ ] 完整測試所有功能
- [ ] 處理錯誤情況和例外
- [ ] 優化查詢效能
- [ ] 設定 Firebase 安全規則

## 回滾（不建議）

如果需要回滾到 MySQL（不建議，因為已完全移除）：

1. 切換回 `main` 分支：`git checkout main`
2. 恢復 `settings.py` 中的 MySQL 設定
3. 恢復 `views.py` 中的 ORM 操作
4. 重新安裝 PyMySQL 或 mysqlclient

**注意**：回滾會失去所有 Firebase 中的資料，請謹慎操作。

## 參考資料

- [Firebase Admin SDK 文件](https://firebase.google.com/docs/admin/setup)
- [Firestore 文件](https://firebase.google.com/docs/firestore)
- [Firebase Console](https://console.firebase.google.com/)

<<<<<<< HEAD
## 相關文件

- `完全使用Firebase設定完成.md` - 完整遷移記錄
- `網頁功能測試步驟指南.md` - 功能測試指南
- `README.md` - 專案基本說明

---

## ✨ 遷移完成！

您的專案現在已**完全使用 Firebase Firestore**，享受 Firebase 的強大功能和可擴展性！

🎉
=======

>>>>>>> f679c86087e0e172543b0df1d5f4252e27ad1b6c
