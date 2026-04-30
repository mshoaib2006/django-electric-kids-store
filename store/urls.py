from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('search/', views.search, name='search'),

    # Cart
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

    # Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/<str:order_number>/confirmation/', views.order_confirmation, name='order_confirmation'),

    # Auth
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]
