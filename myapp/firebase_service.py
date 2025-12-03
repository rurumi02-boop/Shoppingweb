import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 確保 Firebase 只初始化一次
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

class FirebaseService:

    @staticmethod
    def get_collection(collection_name):
        return db.collection(collection_name)

    @staticmethod
    def add_document(collection_name, doc_id, data):
        return db.collection(collection_name).document(doc_id).set(data)

    @staticmethod
    def get_document(collection_name, doc_id):
        doc = db.collection(collection_name).document(doc_id).get()
        return doc.to_dict() if doc.exists else None

    # ========== 商品相關方法 ==========
    
    @staticmethod
    def get_products(filters=None):
        """取得商品列表，支援篩選條件"""
        query = db.collection('products')
        
        if filters:
            if 'category_id' in filters:
                query = query.where('category_id', '==', str(filters['category_id']))
            if 'brand_id' in filters:
                query = query.where('brand_id', '==', str(filters['brand_id']))
            if 'is_active' in filters:
                query = query.where('is_active', '==', filters['is_active'])
        
        docs = query.stream()
        products = []
        for doc in docs:
            product_data = doc.to_dict()
            product_data['product_id'] = doc.id
            products.append(product_data)
        return products

    @staticmethod
    def get_product(product_id):
        """取得單一商品"""
        doc = db.collection('products').document(str(product_id)).get()
        if doc.exists:
            product_data = doc.to_dict()
            product_data['product_id'] = doc.id
            return product_data
        return None

    @staticmethod
    def get_new_products(days=30):
        """取得最近新增的商品"""
        cutoff_date = datetime.now() - timedelta(days=days)
        query = db.collection('products').where('is_active', '==', True)
        
        docs = query.stream()
        products = []
        for doc in docs:
            product_data = doc.to_dict()
            product_data['product_id'] = doc.id
            
            # 檢查創建日期
            created_at = product_data.get('created_at')
            if created_at and isinstance(created_at, datetime):
                if created_at >= cutoff_date:
                    products.append(product_data)
            elif not created_at:
                # 如果沒有創建日期，也加入列表
                product_data['created_at'] = datetime.min
                products.append(product_data)
        
        return products

    @staticmethod
    def create_product(product_data):
        """創建新商品"""
        product_data['created_at'] = datetime.now()
        product_data['updated_at'] = datetime.now()
        doc_ref = db.collection('products').document()
        doc_ref.set(product_data)
        return doc_ref.id

    # ========== 分類相關方法 ==========
    
    @staticmethod
    def get_all_categories():
        """取得所有分類"""
        docs = db.collection('categories').stream()
        categories = []
        for doc in docs:
            category_data = doc.to_dict()
            category_data['category_id'] = doc.id
            categories.append(category_data)
        return categories

    @staticmethod
    def get_category_by_id(category_id):
        """根據 ID 取得分類"""
        doc = db.collection('categories').document(str(category_id)).get()
        if doc.exists:
            category_data = doc.to_dict()
            category_data['category_id'] = doc.id
            return category_data
        return None

    # ========== 品牌相關方法 ==========
    
    @staticmethod
    def get_all_brands():
        """取得所有品牌"""
        docs = db.collection('brands').stream()
        brands = []
        for doc in docs:
            brand_data = doc.to_dict()
            brand_data['brand_id'] = doc.id
            brands.append(brand_data)
        return brands

    @staticmethod
    def get_or_create_brand(brand_name):
        """取得或創建品牌"""
        # 先嘗試查找現有品牌
        query = db.collection('brands').where('name', '==', brand_name).limit(1)
        docs = list(query.stream())
        
        if docs:
            return docs[0].id
        else:
            # 創建新品牌
            doc_ref = db.collection('brands').document()
            doc_ref.set({
                'name': brand_name,
                'created_at': datetime.now()
            })
            return doc_ref.id

    # ========== 願望清單相關方法 ==========
    
    @staticmethod
    def is_product_favorited(user_id, product_id):
        """檢查商品是否已加入願望清單"""
        query = db.collection('wishlist').where('user_id', '==', str(user_id)).where('product_id', '==', str(product_id)).limit(1)
        docs = list(query.stream())
        return len(docs) > 0

    @staticmethod
    def toggle_wishlist(user_id, product_id):
        """切換願望清單狀態"""
        query = db.collection('wishlist').where('user_id', '==', str(user_id)).where('product_id', '==', str(product_id)).limit(1)
        docs = list(query.stream())
        
        if docs:
            # 已存在，刪除
            docs[0].reference.delete()
            return False, 'removed'
        else:
            # 不存在，新增
            db.collection('wishlist').document().set({
                'user_id': str(user_id),
                'product_id': str(product_id),
                'created_at': datetime.now()
            })
            return True, 'added'
    
    @staticmethod
    def get_wishlist_by_user(user_id: str) -> List[dict]:
        """取得使用者的我的最愛列表"""
        wishlist = db.collection('wishlist').where('user_id', '==', user_id).stream()
        result = []
        for item in wishlist:
            item_data = item.to_dict()
            # 取得商品資訊
            product = FirebaseService.get_product(item_data.get('product_id'))
            if product:
                result.append({
                    'wishlist_id': item.id,
                    'product': product,
                    'added_at': item_data.get('added_at')
                })
        return result
    
    @staticmethod
    def is_product_favorited(user_id: str, product_id: str) -> bool:
        """檢查商品是否已加入我的最愛"""
        wishlist = db.collection('wishlist').where('user_id', '==', user_id).where('product_id', '==', product_id).limit(1).stream()
        return len(list(wishlist)) > 0
    
    # ========== Review 操作 ==========
    @staticmethod
    def get_reviews_by_product(product_id: str) -> List[dict]:
        """取得商品的評價列表"""
        try:
            reviews = db.collection('reviews').where('product_id', '==', str(product_id)).stream()
            result = []
            for review in reviews:
                review_data = review.to_dict()
                # 取得使用者資訊
                user_id = review_data.get('user_id')
                if user_id:
                    user = FirebaseService.get_user_by_id(str(user_id))
                    if user:
                        review_data['user'] = user
                review_data['review_id'] = review.id
                result.append(review_data)
            # 按日期排序（最新的在前）
            result.sort(key=lambda x: x.get('review_date', datetime.min), reverse=True)
            return result
        except Exception as e:
            print(f"取得評價時發生錯誤: {e}")
            return []
    
    @staticmethod
    def create_review(review_data: dict) -> str:
        """創建評價"""
        doc_ref = db.collection('reviews').document()
        review_data['review_date'] = datetime.now()
        doc_ref.set(review_data)
        return doc_ref.id

    @staticmethod
    def get_wishlist_by_user(user_id):
        """取得用戶的願望清單"""
        query = db.collection('wishlist').where('user_id', '==', str(user_id))
        docs = query.stream()
        
        wishlist = []
        for doc in docs:
            wishlist_data = doc.to_dict()
            product_id = wishlist_data.get('product_id')
            if product_id:
                product = FirebaseService.get_product(product_id)
                if product:
                    wishlist_data['product'] = product
                    wishlist.append(wishlist_data)
        
        return wishlist

    # ========== 訂單相關方法 ==========
    
    @staticmethod
    def create_order(order_data):
        """創建訂單"""
        order_data['created_at'] = datetime.now()
        order_data['updated_at'] = datetime.now()
        doc_ref = db.collection('orders').document()
        doc_ref.set(order_data)
        return doc_ref.id

    @staticmethod
    def create_order_item(item_data):
        """創建訂單項目"""
        item_data['created_at'] = datetime.now()
        doc_ref = db.collection('order_items').document()
        doc_ref.set(item_data)
        return doc_ref.id

    @staticmethod
    def get_orders_by_user(user_id):
        """取得用戶的訂單"""
        query = db.collection('orders').where('user_id', '==', str(user_id)).order_by('created_at', direction=firestore.Query.DESCENDING)
        docs = query.stream()
        
        orders = []
        for doc in docs:
            order_data = doc.to_dict()
            order_data['order_id'] = doc.id
            
            # 取得訂單項目
            items_query = db.collection('order_items').where('order_id', '==', doc.id)
            items_docs = items_query.stream()
            
            order_items = []
            for item_doc in items_docs:
                item_data = item_doc.to_dict()
                product_id = item_data.get('product_id')
                if product_id:
                    product = FirebaseService.get_product(product_id)
                    if product:
                        item_data['product'] = product
                order_items.append(item_data)
            
            order_data['items'] = order_items
            orders.append(order_data)
        
        return orders

    # ========== 評價相關方法 ==========
    
    @staticmethod
    def get_reviews_by_product(product_id):
        """取得商品的評價"""
        query = db.collection('reviews').where('product_id', '==', str(product_id))
        docs = query.stream()
        
        reviews = []
        for doc in docs:
            review_data = doc.to_dict()
            review_data['review_id'] = doc.id
            reviews.append(review_data)
        
        return reviews

    # ========== 用戶相關方法 ==========
    
    @staticmethod
    def create_user(user_data):
        """創建用戶"""
        user_data['created_at'] = datetime.now()
        doc_ref = db.collection('users').document()
        doc_ref.set(user_data)
        return doc_ref.id