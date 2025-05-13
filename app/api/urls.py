from django.urls import path
from .views import Students, ContactListView, ContactUpdateDetailView
from .exam_views import ChatView
from .shop_views import ProductView, CartView, CheckoutView, CategoryView

urlpatterns = [
    # Student endpoints
    path('students/', Students.as_view(), name='list_of_students'),
    
    # Contact endpoints
    path('contact/', ContactListView.as_view(), name='contact_new'),
    path('contact/<int:contact_id>/', ContactListView.as_view(), name='contact_detail'),
    path('contacts/', ContactListView.as_view(), name='contact_list'),
    path('contacts/<int:contact_id>/', ContactUpdateDetailView.as_view(), name='contact_update_detail'),
    
    # Chat endpoint
    path('chat/', ChatView.as_view(), name='chat_view'),
    
    # Shop endpoints (fixed)
    path('shop/', ProductView.as_view(), name='product_view'),
    path('products/', ProductView.as_view(), name='product_list'),
    path('cart/', CartView.as_view(), name='cart_view'),  # Changed from chat/
    path('checkout/', CheckoutView.as_view(), name='checkout_view'),  # Changed from chat/
    
    # Category endpoint
    path('categories/', CategoryView.as_view(), name='category_list'),
]