from django.conf import settings
from django.shortcuts import render,redirect
from django.views import View
import razorpay
from .models import OrderPlaced, Payment, Product,Customer,Cart, Wishlist
from .forms import ProfileForm, RegistrationForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

@login_required
def home(request):    
      
    product = Product.objects.all()
    return render(request,"index.html",locals())

@login_required
def about(request):
    context = {
        "title":"About Us"
    }
    return render(request,"about.html",context)

@login_required
def contact(request):
    context = {
        "title":"Contact Us"
    }
    return render(request,"contact.html",context)

@method_decorator(login_required,name = 'dispatch')
class Category(View):
    def get(self,request,value):       
        product = Product.objects.filter(category = value)
        title = Product.objects.filter(category = value).values('title')
        return render(request,"category.html",locals())

@method_decorator(login_required,name = 'dispatch')    
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user = request.user))
        return render(request,"productdetails.html",locals())

@method_decorator(login_required,name = 'dispatch')    
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.get(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"category.html",locals())

@method_decorator(login_required,name = 'dispatch')    
class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"category.html",locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = RegistrationForm()
        return render(request,"customerregistration.html",locals())
    def post(self,request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Registered Successfully.")
        else:
            messages.warning(request,"Invalid input data.")
        return render(request,"customerregistration.html",locals())
    
@method_decorator(login_required,name = 'dispatch')    
class ProfileView(View):
    def get(self,request):
        profile = Customer.objects.filter(user = request.user).first()
        form = ProfileForm(instance=profile)
        return render(request,'profile.html',locals())
    def post(self,request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile saved successfully.")
        else:
            messages.warning(request,"Invalid Input Data.")
        return render(request,'profile.html',locals())
    
@login_required
def address(request):
     add = Customer.objects.filter(user = request.user)
     return render(request, 'address.html',locals())

@method_decorator(login_required,name = 'dispatch')
class UpdateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = ProfileForm(instance=add)
        return render(request, 'updateAddress.html',locals())
    def post(self,request,pk):
        form = ProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations, Profile Updated successfully.")
        else:
            messages.warning(request,"Invalid input data.")
        return redirect("address")
    
def deleteAddress(request):
    def post(self,request,pk):
        address = Customer.objects.get(pk=pk)
        address.delete()
    return redirect('address')

# @login_required 
# def add_to_cart(request):
#     user = request.user 
#     product_id = request.GET.get('prod_id')
#     product = Product.objects.get(id=product_id)
#     cartitem = Cart(user=user,product=product)
#     cartitem.save()
#     return redirect("/cart")

@login_required 
def add_to_cart(request):
    user = request.user 
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    print("Products to add = ",product)
    
    cart = Cart.objects.all().filter(user=user)
    print("cart = ",cart)
    product_list = list(cart.values_list('product__title'))
    print("product_list = ",product_list)
    
    name_of_product = [d[0] for d in product_list]
    # print(name_of_product)
    
    # for i in product_list:
    #     product_list.extend(list(i))
    #     print(product_list)
        
    if str(product) in name_of_product:
        cart_new_obj = Cart.objects.get(user=user,product=product)
        cart_new_obj.quantity += 1
        cart_new_obj.save()
        print("cart_new_obj=",cart_new_obj)
        print("inside if")
    else:
        Cart(user=user,product=product).save()
        print("outside if")
    return redirect("/cart")

@login_required 
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user = user)
    amount = 0
    for p in cart:
        if p.quantity > 0: 
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        if p.quantity > 0:
            totalamount = amount + 40
        else:
            totalamount = 0
    return render(request,'addToCart.html',locals())

@method_decorator(login_required,name = 'dispatch')
class Checkout(View):
    def get(self,request):
        user = request.user
        address = Customer.objects.filter(user = user)
        cart_items = Cart.objects.filter(user = user)
        amount = 0        
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data = {"amount":razoramount,"currency":"INR","receipt":"order_rcptid_12"}
        payment_response = client.order.create(data = data)
        # print(payment_response) 
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status,
            )
            payment.save()
        return render(request,'checkout.html',locals())
    
def plus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = product_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        cart = Cart.objects.filter(user = request.user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value  
        totalamount = amount + 40        
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
       
def minus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        cart = Cart.objects.filter(user = request.user)
        amount = 0
        for p in cart:
            if p.quantity != 0:
                value = p.quantity * p.product.discounted_price
                amount = amount + value
                totalamount = amount + 40
            else:
                totalamount = amount + 0  
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@login_required 
def remove_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.delete()
        cart = Cart.objects.filter(user = request.user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40   
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@login_required 
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    # product = Product.objects.GET['prod_id']
    # orderplaced = OrderPlaced.objects.create(user=request.user,customer=customer,product=Product.title,quantity=OrderPlaced.quantity,ordered_date=OrderPlaced.ordered_date,status=OrderPlaced.status,payment=OrderPlaced.payment)
    # orderplaced.save()
    cart = Cart.objects.filter(user = request.user)
    for c in cart:
        OrderPlaced(user=request.user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("orders/")

@login_required 
def orders(request):
    order_placed=OrderPlaced.objects.filter(user = request.user)
    return render(request,'orders.html',locals())

@login_required 
def plus_wishlist(request):
    if request.method == "GET": 
        prod_id=request.GET['prod_id']
        product = Product.objects.get(id='prod_id')
        Wishlist(user = request.user,product=product).save()
        data = {
            "message":"Item added to Wishlist Successfully."
            }
        return JsonResponse(data)
    
@login_required 
def minus_wishlist(request):
    if request.method == "GET": 
        prod_id=request.GET['prod_id']
        product = Product.objects.get(id='prod_id')
        Wishlist(user = request.user,product=product).delete()
        data = {
            "message":"Item removed from Wishlist Successfully."
            }
        return JsonResponse(data)
    

def search(request):
    query = request.GET['search']
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,'search.html',locals())

def wishlist(request):
    return render(request,'wishlist.html')
