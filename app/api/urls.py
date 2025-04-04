from django.urls import path
#from .views import HelloWorld
from .views import Students
from .views import ContactListView
from .views import ContactUpdateDetailView
from .exam_views import ChatView
from .shop_views import ProductView
from .shop_views import CartView
from .shop_views import CheckoutView

urlpatterns = [
    #path('hello/', HelloWorld.as_view(), name='hello_world'),
    path('students/', Students.as_view(), name='list_of_students'),
    path('contact/', ContactListView.as_view(), name='contact_new'),
    path('contact/<int:contact_id>/', ContactListView.as_view(), name='contact_detail'),
    path('contacts/', ContactListView.as_view(), name='contact_list'),
    path('contacts/<int:contact_id>/', ContactUpdateDetailView.as_view(), name='contact_update_detail'),
    path('chat/', ChatView.as_view(), name='chat_view'),
    path('shop/', ProductView.as_view(), name='product_view'),
    path('chat/', CartView.as_view(), name='cart_view'),
    path('chat/', CheckoutView.as_view(), name='checkout_view'),
]

