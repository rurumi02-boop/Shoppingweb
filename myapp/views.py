from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category, Brand, Wishlist, User, Order, OrderItem
from django.db.models import Q
from myapp.models import Category 
from datetime import timedelta, datetime
from django.utils import timezone
from .forms import RegistrationForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import *
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import User as CustomUser
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from .firebase_service import FirebaseService
def home(request):
    
    categories = [
        ('3C與筆電', 1),
        ('手機平板與周邊', 2),
        ('服飾', 3),
        ('男女鞋', 4),
        ('機車', 5),
        ('包包/精品/配件', 6),
        ('居家生活', 7),
        ('嬰幼童商品', 8),
        ('茶葉', 9),
        ('戶外/旅行', 10),
    ]
    category_products = {}
    for name, cat_id in categories:
        # 使用 Firebase 取得商品
        products = FirebaseService.get_products({'category_id': cat_id, 'is_active': True})
        category_products[cat_id] = products

    return render(request, 'home.html', {
        'categories': categories,
        'category_products': category_products,
        
    })




def new_products(request):
    recent_days = 30  # 可調整為 7、14、30 天
    # 使用 Firebase 取得新商品
    new_products = FirebaseService.get_new_products(days=recent_days)
    # 按創建時間排序（降序）
    new_products.sort(key=lambda x: x.get('created_at', datetime.min), reverse=True)

    return render(request, 'products/new_products.html', {
        'new_products': new_products,
        'recent_days': recent_days,
    })


# 商品列表（支援分類、品牌、關鍵字搜尋）
class ProductListView(ListView):
    template_name = 'products/product_list.html'  # 對應的 HTML 模板檔案
    context_object_name = 'products'  # 在模板中可用變數名稱為 products
    paginate_by = 10  # 每頁顯示 10 個產品

    def get_queryset(self): # 覆寫 get_queryset 方法：決定要顯示哪些商品
        # 使用 Firebase 取得商品
        filters = {'is_active': True}
        
        # 篩選參數 從網址參數中取得使用者輸入的篩選條件
        category_id = self.request.GET.get('category')
        brand_id = self.request.GET.get('brand')
        keyword = self.request.GET.get('q') #對應到product_list name='q'

        # 若有選擇分類，則篩選對應分類的商品
        if category_id:
            filters['category_id'] = int(category_id)
        if brand_id:
            filters['brand_id'] = int(brand_id)
        
        # 取得商品列表
        products = FirebaseService.get_products(filters)
        
        # 若有輸入關鍵字，則從產品名稱中模糊搜尋
        if keyword:
            products = [p for p in products if keyword.lower() in p.get('product_name', '').lower()]

        return products

    # 加入額外變數提供給模板使用（例如：分類清單、品牌清單等）
    def get_context_data(self, **kwargs):
        # 取得商品列表
        products = self.get_queryset()
        
        # 手動分頁
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            products_page = paginator.page(page)
        except PageNotAnInteger:
            products_page = paginator.page(1)
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)
        
        # 建立 context
        context = {
            'products': products_page,
            'page_obj': products_page,  # 分頁物件
            'all_categories': FirebaseService.get_all_categories(),
            'all_brands': FirebaseService.get_all_brands(),
            'selected_category': self.request.GET.get('category', ''),
            'selected_brand': self.request.GET.get('brand', ''),
            'keyword': self.request.GET.get('q', ''),
        }

        return context
    
    


# # 商品詳情頁：顯示單一商品的詳細資訊
class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        # 從 URL 參數取得商品 ID
        product_id = self.kwargs.get('pk')
        product = FirebaseService.get_product(str(product_id))
        if not product:
            from django.http import Http404
            raise Http404("商品不存在")
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()  # 取得當前商品

        if self.request.user.is_authenticated:
            user_id = str(self.request.user.id) if hasattr(self.request.user, 'id') else None
            product_id = product.get('product_id')
            if user_id and product_id:
                # 使用 Firebase 檢查是否已加入最愛
                context['is_favorited'] = FirebaseService.is_product_favorited(user_id, product_id)
            else:
                context['is_favorited'] = False
        else:
            context['is_favorited'] = False

        # 取得商品評等和評價
        product_id = product.get('product_id')
        if product_id:
            reviews = FirebaseService.get_reviews_by_product(str(product_id))
            context['reviews'] = reviews
            
            # 計算平均評等
            if reviews:
                valid_ratings = [r.get('rating', 0) for r in reviews if r.get('rating')]
                if valid_ratings:
                    total_rating = sum(valid_ratings)
                    context['average_rating'] = round(total_rating / len(valid_ratings), 1)
                    context['review_count'] = len(valid_ratings)
                else:
                    context['average_rating'] = 0.0
                    context['review_count'] = 0
            else:
                context['average_rating'] = 0.0
                context['review_count'] = 0
        else:
            context['reviews'] = []
            context['average_rating'] = 0.0
            context['review_count'] = 0

        return context



#露營活動
def activity(request):
    return render(request, 'activity.html') 

#連絡資訊
def contact(request):
    return render(request, 'contact.html')  
#公司地點
def locations(request):
    return render(request, 'locations.html')   
#退貨規定公告
def returnNotice(request):
    return render(request, 'returnNotice.html') 

#-----------------------------------------------------------------
#會員區設定

#登入
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

def userlogin(request):
    next_url = request.GET.get('next', '/home/')  # 沒有 next 就回首頁

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(f"DEBUG: authenticate 回傳 user = {user}")

        if user is not None:
            login(request, user)

            # 防止 open redirect 攻擊，確保 next_url 合法
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            else:
                return redirect('/home/')
        else:
            messages.error(request, '❌登入失敗，帳號或密碼錯誤！')
            return render(request, 'userlogin.html', {'next': next_url})

    return render(request, 'userlogin.html', {'next': next_url})

#註冊=#增加使用者useradd
def register(request): 
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        print(f"username={username},password={password},repassword={repassword},email={email},phone={phone}")
        
        #檢查帳號是否存在（檢查 Django User 表，因為認證使用 Django）
        if User.objects.filter(username=username).exists():
            messages.error(request, "帳號己被使用,請重新填寫")
            return render(request, "register.html")
         #檢查密碼否一致
        if password != repassword:
            messages.error(request, "密碼輸入不同,請重新輸入")
            return render(request, "register.html")

        #驗證成功 - 使用 Django User 模型（保留 Django Auth）
        user = User.objects.create_user(username=username,password=password,email=email)
        user.is_staff=False
        user.is_active=True
        user.phone = phone
        user.save()
        
        # 同時在 Firebase 中創建使用者記錄
        try:
            FirebaseService.create_user({
                'username': username,
                'email': email,
                'phone': phone,
                'django_user_id': user.id,  # 關聯到 Django User
            })
        except Exception as e:
            print(f"Firebase 使用者創建失敗：{e}")
        
        messages.success(request,"註冊成功,請登入,將為您導向登入頁面")
        return redirect("userlogin")

    else:
        return render(request, "register.html")

#登出
def logout_user(request):
    logout(request)              #會清除 session，登出目前的使用者
    return redirect('home')

#使用者介面
@login_required
def user_info(request):
    user = request.user  # 已是自訂的 User 實例（含 phone、address）
    user_id = str(user.id) if hasattr(user, 'id') else None

    # 最愛商品（使用 Firebase）
    favorites = []
    if user_id:
        favorites = FirebaseService.get_wishlist_by_user(user_id)

    # 訂單及關聯商品（使用 Firebase）
    orders = []
    if user_id:
        orders = FirebaseService.get_orders_by_user(user_id)

    return render(request, 'user_info.html', {
        'user': user,
        'orders': orders,
        'favorites': favorites,
    })



#使用者介面修改密碼
@login_required
def custom_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # 保持登入狀態
            messages.success(request, '✅ 密碼已成功更新！')
            return redirect('user_info')  # 修改為你要導向的頁面
        else:
            messages.error(request, '❌ 發生錯誤，請確認欄位是否正確填寫。')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'reset/my_password_change_form.html', {
        'form': form
    })



#購物車--------------------------------------------------------------------
def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        variant = request.POST.get('variant', '')  # 商品變體（顏色、尺寸等）
    else:
        quantity = 1
        variant = ''
    
    cart = request.session.get("cart", {})
    # 🔹 獲取產品資料，確保 `product_name` 和 `price` 正確存入購物車
    product = FirebaseService.get_product(str(product_id))
    if not product:
        messages.error(request, "商品不存在")
        return redirect('product_list')
    
    # 使用變體作為 key 的一部分（如果有的話）
    cart_key = f"{product_id}_{variant}" if variant else str(product_id)
    
    if cart_key not in cart:
        cart[cart_key] = {
            "quantity": quantity,
            "product_name": product.get('product_name', ''),
            "price": int(product.get('price', 0)),
            "variant": variant,
            "product_id": str(product_id)
        }
    else:
        cart[cart_key]["quantity"] += quantity
    
    request.session["cart"] = cart
    request.session.modified = True
    messages.success(request, f"✅ 已將 {product.get('product_name', '商品')} 加入購物車")
    return redirect('view_cart')

# 直接購買
@login_required
def buy_now(request, product_id):
    """直接購買功能：將商品加入購物車並跳轉到結帳頁面"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        variant = request.POST.get('variant', '')
    else:
        quantity = 1
        variant = ''
    
    product = FirebaseService.get_product(str(product_id))
    if not product:
        messages.error(request, "商品不存在")
        return redirect('product_list')
    
    # 將商品加入購物車
    cart = request.session.get("cart", {})
    cart_key = f"{product_id}_{variant}" if variant else str(product_id)
    cart[cart_key] = {
        "quantity": quantity,
        "product_name": product.get('product_name', ''),
        "price": int(product.get('price', 0)),
        "variant": variant,
        "product_id": str(product_id)
    }
    request.session["cart"] = cart
    request.session.modified = True
    
    # 直接跳轉到結帳頁面
    return redirect('checkout')


def view_cart(request):
    session_cart = request.session.get('cart', {})
    cart_items = {}
    total = 0
    for product_id, item in session_cart.items():
        try:
            price = int(item.get('price', 0) or 0)  #modify
        except (ValueError, TypeError):
            price = 0.0
        try:
            quantity = int(item.get('quantity', 0) or 0)
        except (ValueError, TypeError):
            quantity = 0
        subtotal = price * quantity
        cart_items[product_id] = {
            'product_name': item.get('product_name', '❌ 未知商品'),
            'price': price,
            'quantity': quantity,
            'subtotal': subtotal
        }
        total += subtotal
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'cart.html', context)


def clear_cart(request):
    if request.method == "POST":
        request.session["cart"] = {}
        request.session.modified = True
        request.session['flash_message'] = "🧹 購物車已成功清空。"
        request.session['flash_level'] = "success"
    else:
        request.session['flash_message'] = "❌ 無效的請求方法。"
        request.session['flash_level'] = "error"
    return redirect('view_cart')


def update_cart(request):
    if request.method == "POST":
        cart = request.session.get("cart", {})

        for key, value in request.POST.items():
            if key.startswith("quantity_"):
                product_id = key.split("_", 1)[1]
                try:
                    quantity = int(value)
                    if quantity > 0 and product_id in cart:
                        cart[product_id]["quantity"] = quantity
                except ValueError:
                    continue

        request.session["cart"] = cart
        request.session.modified = True

        if request.POST.get('go_to_checkout') == '1':
            return redirect('checkout')

    return redirect('view_cart')


def remove_from_cart(request, product_id):
    print(f"[DEBUG] method: {request.method}, product_id: {product_id}")
    if request.method == "POST":
        cart = request.session.get("cart", {})
        product_id_str = str(product_id)
        if product_id_str in cart:
            del cart[product_id_str]
            request.session["cart"] = cart
            request.session.modified = True
            print(f"Cart after deletion: {cart}")
            request.session['flash_message'] = "✅ 已成功移除商品。"
            request.session['flash_level'] = "success"
        else:
            request.session['flash_message'] = "⚠️ 找不到指定的商品，無法移除。"
            request.session['flash_level'] = "warning"
    else:
        request.session['flash_message'] = "❌ 無效的請求方法。"
        request.session['flash_level'] = "error"
    return redirect('view_cart')


def checkout(request):
    session_cart = request.session.get('cart', {})
    cart_items = {}
    total = 0
    for product_id, item in session_cart.items():
        price = int(item.get('price', 0) or 0)  #modify
        quantity = int(item.get('quantity', 0) or 0)
        subtotal = price * quantity
        cart_items[product_id] = {
            'product_name': item.get('product_name', '❌ 未知商品'),
            'price': price,
            'quantity': quantity,
            'subtotal': subtotal
        }
        total += subtotal
    context = {
        'cart_items': cart_items,
        'total': total,
        'flash_message': request.session.pop('flash_message', None),
        'flash_level': request.session.pop('flash_level', 'info'),
    }
    return render(request, 'checkout.html', context)
#--------------------------------------------------------

from decimal import Decimal
@login_required(login_url='userlogin')
def submit_order(request):
    if request.method == 'POST':
        user = request.user
        user_id = str(user.id) if hasattr(user, 'id') else None
        cart = request.session.get('cart', {})

        if not user_id:
            messages.error(request, "使用者資訊錯誤")
            return redirect('checkout')

        total_amount = 0
        order_items_data = []
        
        for product_id, item_info in cart.items():
            quantity = item_info.get('quantity', 0)
            product = FirebaseService.get_product(str(product_id))
            if product:
                price = int(product.get('price', 0))
                total_amount += price * quantity
                order_items_data.append({
                    'product_id': str(product_id),
                    'quantity': quantity,
                    'price_at_purchase': price,
                })

        # 創建訂單（使用 Firebase）
        order_data = {
            'user_id': user_id,
            'total_amount': total_amount,
            'shipping_address': request.POST.get('shipping_address'),
            'shipping_city': request.POST.get('shipping_city', ''),
            'shipping_state_province': request.POST.get('shipping_state_province', ''),
            'shipping_zip_code': request.POST.get('shipping_zip_code', ''),
            'shipping_country': request.POST.get('shipping_country', ''),
            'payment_method': request.POST.get('payment_method', ''),
            'order_status': '待處理',
            'payment_status': '未支付',
        }
        
        order_id = FirebaseService.create_order(order_data)
        
        # 創建訂單項目
        for item_data in order_items_data:
            item_data['order_id'] = order_id
            FirebaseService.create_order_item(item_data)

        request.session['cart'] = {}
        messages.success(request, "訂單已成功建立！")
        return redirect('order_success')

    return redirect('checkout')


def order_success(request):
    return render(request, 'order_success.html')


def order_list(request):
    if request.user.is_authenticated:
        # 確保 request.user 是有效的 User 實例
        try:
            user = User.objects.get(username=request.user.username)  # 確保是有效的 User
            orders = Order.objects.filter(user=user)
        except User.DoesNotExist:
            orders = Order.objects.none()
    else:
        orders = Order.objects.none()  # 如果未登入，返回空訂單
    
    return render(request, "order_list.html", {"orders": orders})

#--------------------------------------------------------
#加入我的最愛
# @login_required
# def toggle_wishlist(request, product_id):
#     if request.method == 'POST':
#         product = get_object_or_404(Product, pk=product_id)
#         user = CustomUser.objects.get(username=request.user.username)
#         wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)

#         if not created:
#             wishlist_item.delete()
#             status = 'removed'
#         else:
#             status = 'added'

#         return JsonResponse({'status': status})
    
#     return JsonResponse({'error': 'Invalid request'}, status=400)  
 

# @login_required
# def my_wishlist(request):
#     items = Wishlist.objects.filter(user=request.user).select_related('product')
#     return render(request, 'wishlist_list.html', {'items': items})

from django.contrib.auth import REDIRECT_FIELD_NAME
def toggle_wishlist(request, product_id):
    if not request.user.is_authenticated:
        login_url = f"/userlogin/?{REDIRECT_FIELD_NAME}=/user_info/#wishlist"
        return JsonResponse({'redirect': login_url}, status=401)

    if request.method == 'POST':
        user_id = str(request.user.id) if hasattr(request.user, 'id') else None
        if not user_id:
            return JsonResponse({'error': 'Invalid user'}, status=400)
        
        # 使用 Firebase 切換我的最愛
        is_added, status = FirebaseService.toggle_wishlist(user_id, str(product_id))
        
        return JsonResponse({'status': status})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def product_editor(request):
    categories = [
        ('帳篷類Tent', 1),
        ('寢具類Bed', 2),
        ('廚具類KitchenWare', 3),
        ('爐具類Pot', 4),
        ('桌椅類Tables/Chairs', 5),
        ('燈具類Lamp', 6),
        ('保冷類Cooling', 7),
        ('保暖類Warming', 8),
        ('收納類Containers', 9),
        ('其他小物Others', 10),
    ]
    category_products = {}
    for name, cat_id in categories:
        # 使用 Firebase 取得商品
        category_products[cat_id] = FirebaseService.get_products({'category_id': cat_id})

    return render(request, "product_editor.html", {
        'categories': categories,
        'category_products': category_products
        }
    )

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

def submit_product_add(request):
    categories = [
        ('帳篷類Tent', 1),
        ('寢具類Bed', 2),
        ('廚具類KitchenWare', 3),
        ('爐具類Pot', 4),
        ('桌椅類Tables/Chairs', 5),
        ('燈具類Lamp', 6),
        ('保冷類Cooling', 7),
        ('保暖類Warming', 8),
        ('收納類Containers', 9),
        ('其他小物Others', 10),
    ]
    category_products = {}
    for name, cat_id in categories:
        category_products[cat_id] = Product.objects.filter(category_id=cat_id)
    success_message = None
    error_message = None

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description', '')
        price = request.POST.get('price', '0')
        stock_quantity = request.POST.get('stock_quantity', '0')
        sku = request.POST.get('sku', '')
        weight = request.POST.get('weight', '')
        dimensions = request.POST.get('dimensions', '')
        material = request.POST.get('material', '')
        suitable_season = request.POST.get('suitable_season', '')
        capacity = request.POST.get('capacity', '')
        category_id = request.POST.get('category')
        brand_name = request.POST.get('brand')

        # 防呆：分類必填
        if not category_id:
            error_message = "❌ 請選擇商品分類，商品未新增。"
        else:
            # 取得分類（使用 Firebase）
            category = FirebaseService.get_category_by_id(int(category_id))
            if not category:
                error_message = "❌ 分類不存在，商品未新增。"
            else:
                # brand 可能是輸入的名稱或 id；若找不到則建立新品牌
                brand_id = None
                brand_input = brand_name.strip() if brand_name else ''
                if brand_input:
                    brand_id = FirebaseService.get_or_create_brand(brand_input)

                # 檔案上傳處理
                image_url = ''
                image_file = request.FILES.get('image_url')
                if image_file:
                    filename = default_storage.save(
                        os.path.join('product_images', image_file.name),
                        ContentFile(image_file.read())
                    )
                    image_url = default_storage.url(filename)

                # 使用 Firebase 創建商品
                product_data = {
                    'product_name': product_name,
                    'description': description,
                    'price': int(price) if price else 0,
                    'stock_quantity': int(stock_quantity) if stock_quantity else 0,
                    'sku': sku,
                    'image_url': image_url,
                    'weight': weight,
                    'dimensions': dimensions,
                    'material': material,
                    'suitable_season': suitable_season,
                    'capacity': capacity,
                    'category_id': str(category_id),
                    'brand_id': brand_id,
                    'is_active': True
                }
                
                FirebaseService.create_product(product_data)
                success_message = "✅ 新增完成"

    return render(request, "product_editor.html", {
        'categories': categories,
        'category_products': category_products,
        'success_message': success_message,
        'error_message': error_message,
        }
    )
