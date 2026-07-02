from django.urls import path
from .views import (
    CartView, CartClearView,
    CheckoutView, OrderListView, OrderDetailView,
    OrderCancelView, OrderStatusView
)

app_name = 'orders'

urlpatterns = [
    # Panier
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/clear/', CartClearView.as_view(), name='cart-clear'),
    path('cart/remove/<str:item_key>/', CartView.as_view(), name='cart-remove'),

    # Commandes
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:order_id>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
    path('orders/status/<str:order_number>/', OrderStatusView.as_view(), name='order-status'),
]
