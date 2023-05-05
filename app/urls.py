from django.urls import path,include
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from app.forms import LoginForm,ResetPassword,ChangePasswordForm
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home),
    path('category/<slug:value>',views.Category.as_view(),name = "category"),
    path('product-detail/<slug:pk>',views.ProductDetail.as_view(),name = "product-detail"),
    path('category-title/<val>',views.CategoryTitle.as_view(),name = "category-title"),
    path('about-us', views.about,name = "about"),
    path('contact-us', views.contact,name = "contact"),
    
    path('profile/', views.ProfileView.as_view(),name = "profile"),
    path('', views.add_comment, name='add_comment'),
    path('address/', views.address,name = "address"),
    path('update-address/<int:pk>',views.UpdateAddress.as_view(),name = 'updateAddress'),
    path('delete-address/<int:pk>',views.deleteAddress,name='delete_address'),    
    #login 
    path('registration', views.CustomerRegistrationView.as_view(),name = "customerregistration"),
    path('verify/<slug>',views.verify,name = "verify"),
    path('accounts/login/', auth_view.LoginView.as_view(template_name = "login.html"),name = "loginuser"),
    path('accounts/', include('allauth.urls')),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name = "passwordreset.html",form_class = ResetPassword),name = "password_reset"),
        
    #logout
    path('logout/',auth_view.LogoutView.as_view(next_page="loginuser"),name = "logout"),
    
    path('change-password/',auth_view.PasswordChangeView.as_view(template_name='change_password.html',form_class=ChangePasswordForm,success_url='/passChangeDone'), name='change_password'),
    path('passChangeDone/',auth_view.PasswordChangeDoneView.as_view(template_name='passChangeDone.html'), name='passChangeDone'),

    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('pluswishlist/',views.plus_wishlist),
    path('minuswishlist/',views.minus_wishlist),
    
    # #addtocart
    path('add-to-cart/', views.add_to_cart,name = "addtocart"),
    path('cart',views.show_cart,name = "showcart"),
    path('checkout/',views.Checkout.as_view(),name = "checkout"),
    path('paymentdone/',views.payment_done,name = "paymentdone"),
    path('orders',views.orders,name = 'orders'),
    
    path('search/',views.search,name = "search"),
    path('wishlist',views.wishlist,name = "wishlist"),

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
