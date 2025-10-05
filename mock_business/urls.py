from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    OrderListView, OrderDetailView,
    StoreListView, StoreDetailView,
    UserListView, UserDetailView
)

urlpatterns = [
    # Products
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    
    # Orders
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    
    # Stores
    path('stores/', StoreListView.as_view(), name='store-list'),
    path('stores/<int:pk>/', StoreDetailView.as_view(), name='store-detail'),
    
    # Users (read-only mock)
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
