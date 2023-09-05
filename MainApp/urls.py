
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('index',views.index,name="index"),
    path('shop',views.shop,name="shop"),
    path('cart',views.cart,name="cart"),
    path('checkout',views.checkout,name="checkout"),
    path('login',views.login,name="login"),
    path('register',views.register,name="register"),
    path('dash',views.dash,name="dash"),
    path('userdash',views.userdash,name="userdash"),
    path('add_products',views.add_products,name="add_products"),
    path('view_products',views.view_products,name="view_products"),
    path('view_pending',views.view_pending,name="view_pending"),
    path('view_status',views.view_status,name="view_status"),
    path('view_delivered',views.view_delivered,name="view_delivered"),

    path('register_user',views.register_user,name="register_user"),
    path('signin_user',views.signin_user,name="signin_user"),
    path('add_prod_details',views.add_prod_details,name="add_prod_details"),
    path('detail?id=<int:id>',views.detail,name="detail"),
    path('carts?id=<int:id>',views.carts,name="carts"),
    path('add_to_cart',views.add_to_cart,name="add_to_cart"),
    path('place_order',views.place_order,name="place_order"),
    path('process?id=<int:id>',views.process,name="process"),
    path('decline?id=<int:id>',views.decline,name="decline"),
    path('logout',views.logout,name="logout"),
]