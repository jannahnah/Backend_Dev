from django.urls import path
from .shop_views import ProductView

urlpatterns = [
    path('products/', ProductView.as_view(), name='product_view'),
]