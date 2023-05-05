from django.contrib import admin
from app.models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist,CustomUser,CommentSection

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','description','category','product_photo']
    search_fields = ['id','title','selling_price','discounted_price','description','category']
    
admin.site.register(Product,ProductAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email','token','is_verified',]
    
admin.site.register(CustomUser,CustomUserAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode']
    search_fields = ['locality','city','state','zipcode']
    
admin.site.register(Customer,CustomerAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']
    search_fields = ['quantity']
    
admin.site.register(Cart,CartAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']
    search_fields = ['amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

admin.site.register(Payment,PaymentAdmin)    

class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status','payment']
    search_fields = ['quantity','ordered_date','status','payment']
    
admin.site.register(OrderPlaced,OrderPlacedAdmin)    

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id','user','product']
    
admin.site.register(Wishlist,WishlistAdmin)

class CommentSectionAdmin(admin.ModelAdmin):
    list_display = ['name','comment','product','created_at']
    
admin.site.register(CommentSection,CommentSectionAdmin)