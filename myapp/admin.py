from django.contrib import admin
from .models import Product, Category, User, Brand, Order, Review

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id','product_name','sku','price',
                    'stock_quantity',
                    'category','weight','dimensions',
                    'dimensions','suitable_season','is_active')
    list_filter = ('product_name','sku','price',)
    search_fields = ('product_name',)
    ordering=('product_id',)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_id','brand_name','description')
    search_fields = ('brand_name',)
    list_filter = ('brand_name',)

class CategoryAdim(admin.ModelAdmin):
    list_display = ('category_id', 'category_name', 'description', 'parent_category')
    search_fields = ('category_name',)
    list_filter = ('category_name',)

class OrderAdim(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'order_date', 'total_amount','order_status')
    search_fields = ('order_id',)
    list_filter = ('order_id','user','order_date',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'address', 'is_staff', 'is_active')

class ReviewAdim(admin.ModelAdmin):
    list_display = ('user','product','rating','comment','review_date')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category,CategoryAdim)
admin.site.register(Brand,BrandAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Order,OrderAdim)
admin.site.register(Review,ReviewAdim)