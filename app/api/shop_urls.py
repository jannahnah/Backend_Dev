# shop/urls.py
from django.urls import path
from .views import ProductView, CartView, CheckoutView

urlpatterns = [
    path('products/', ProductView.as_view(), name='product-list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]