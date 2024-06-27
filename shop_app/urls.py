
from django.urls import path
from shop_app.views import *

app_name = 'shop_app'

urlpatterns = [
    path('api/v1/products/', ProductAPI.as_view(), name='product-api'),
    path('api/vi/products/<int:pk>/', ProductDetailAPI.as_view(), name='product-detail-api'),
    # path('update/', ProductUpdateAPI.as_view(), name='product-update-api'),
    path('api/vi/orders/', OrderAPI.as_view(), name='order_api'),
    path('api/vi/orders/<int:pk>/cancel/', CancelOrderAPI.as_view(), name='cancel-order-api'),
    path('api/vi/orders-listing/', OrderListAPI.as_view(), name='order-list'), 
]


