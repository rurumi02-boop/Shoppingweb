"""homework1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from myapp.views import custom_change_password
from django.urls import reverse_lazy


urlpatterns = [
    #主頁內容
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),                                 # 主路徑
    path('home/', lambda request: redirect('/')),                      # 將/home/轉回 
    path('contact/', views.contact, name='contact'),                   #聯絡資訊
    path('locations/', views.locations , name='locations'),            #分公司地點
    path('returnNotice/', views.returnNotice , name='returnNotice'),   #退貨需知
    path('products/', include('myapp.urls')),                          #總產品頁面
    path('new_products/', views.new_products, name='new_products'),    #新產品頁面
    path('activity/', views.activity, name='activity'),                #露營活動


    path('register/', views.register, name='register'),                # 註册頁面
    path('userlogin/', views.userlogin, name='userlogin'),             # 使用者登入
    path('logout/', views.logout_user, name='logout'),                 # 使用者登出
    path('user_info/', views.user_info, name='user_info'),             # 使用者介面
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('user/', views.user_info, name='user_info'),

    
    path('products/<int:product_id>/add/', views.add_to_cart, name='add_to_cart'),                   # 加入購物車
    path('products/<int:product_id>/buy-now/', views.buy_now, name='buy_now'),                      # 直接購買
    path('cart/', views.view_cart, name='view_cart'),                                                # 檢視購物車
    path('cart/clear/', views.clear_cart, name='clear_cart'),                                        # 清空購物車
    path('cart/update/', views.update_cart, name='update_cart'),                                     # 更新購物車
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),          # 購物車刪除某件商品
    path('checkout/', views.checkout, name='checkout'),                                              # 購物車結帳
    path('submit-order/', views.submit_order, name='submit_order'),                                  # 送出訂單
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),                    #??
    #path('order/<int:order_id>/', views.order_detail, name='order_detail'), #周新增
    path('order-success/', views.order_success, name='order_success'),                               #成功送出訂單
    #path("my-orders/", views.order_list, name="order_list"),                                         #訂單名細-->合併至user_info


    path('resetpassword/',auth_views.PasswordResetView.as_view(template_name='reset/password_reset.html',
    email_template_name='reset/password_reset_email.html',subject_template_name='reset/password_reset_subject.txt',
    from_email='noreply@pysen-camp.com',success_url='/reset-password/done/',),name='password_reset'), # 密碼重設
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='reset/password_reset_done.html'), name='password_reset_done'),
    path('reset-password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset/password_reset_confirm.html', success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset/password_reset_complete.html'), name='password_reset_complete'),
    path('user/change-password/', custom_change_password,name='custom_change_password'), #己登入的使用者變更密碼用

    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    #path('my_wishlist/', views.my_wishlist, name='my_wishlist'),
    #path('pre_wishlist/<int:product_id>/', views.pre_wishlist, name='pre_wishlist'),
    #path('execute_wishlist/', views.execute_wishlist, name='execute_wishlist'),


    path('products/editor/', views.product_editor, name='product_editor'),
    path('products/submit_product_add/', views.submit_product_add, name='submit_product_add'),

]
