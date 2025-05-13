from django.urls import path, include
from .views import Students, ContactListView, ContactUpdateDetailView
from .exam_views import ChatView

urlpatterns = [
    path('students/', Students.as_view(), name='list_of_students'),
    path('contact/', ContactListView.as_view(), name='contact_new'),
    path('contact/<int:contact_id>/', ContactListView.as_view(), name='contact_detail'),
    path('contacts/', ContactListView.as_view(), name='contact_list'),
    path('contacts/<int:contact_id>/', ContactUpdateDetailView.as_view(), name='contact_update_detail'),
    path('chat/', ChatView.as_view(), name='chat_view'),
    path('shop/', include('api.shop_urls')),
]