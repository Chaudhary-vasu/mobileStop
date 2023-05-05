from datetime import timezone
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser
from app.manager import UserManager

import uuid
# Create your models here.

CATEGORY_CHOICES = (
    ('APL','Apple'),
    ('SMG','Samsung'),
    ('OP','One Plus'),
    ('OPO','Oppo'),
    ('RLM','Realme'),
    ('VO','Vivo'),
)

STATE_CHOICES = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    product_image = models.ImageField(upload_to='product')
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=20)
    
    # for product photo in admin panel
    def product_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.product_image.url))
    product_photo.short_description = "Mobile Image"
    product_photo.allow_tags = True
    
    def __str__(self):
        return self.title  
 
class CustomUser(AbstractUser):
    username = None 
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=200,default="")
    is_verified = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return str(self.email)

class Customer(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    # token = models.CharField(max_length=200)
    # is_verified = models.BooleanField(default=False)
    name = models.CharField(max_length=200,default="",blank=True,null=True)
    locality = models.CharField(max_length=200,blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    mobile = models.IntegerField(default=0,blank=True,null=True)
    zipcode = models.IntegerField(blank=True,null=True)
    state = models.CharField(choices = STATE_CHOICES,max_length=100,blank=True,null=True)

    def __str__(self):
        return str(self.name)
    
# class Customer(models.Model):
#     user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     # email = models.EmailField(unique=True,default="")
#     name = models.CharField(max_length=200)
#     locality = models.CharField(max_length=200)
#     city = models.CharField(max_length=50)
#     mobile = models.IntegerField(default=0)
#     zipcode = models.IntegerField()
#     state = models.CharField(choices = STATE_CHOICES,max_length=100)

#     def __str__(self):
#         return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
class Payment(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)    

class OrderPlaced(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices = STATUS_CHOICES,default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
class CommentSection(models.Model):
    name = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    comment = models.CharField(max_length=2000,default="")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,default='')
    created_at = models.DateTimeField(auto_now_add=True)