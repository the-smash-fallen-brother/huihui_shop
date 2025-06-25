from django.urls import path
from .views import (
    ShoppingCartView,
    ShoppingCartDetailView,
    ShoppingCartCheckAllView,
    ShoppingCartClearView
)

urlpatterns = [
    path('', ShoppingCartView.as_view(), name='cart-list'),
    path('<int:cart_id>/', ShoppingCartDetailView.as_view(), name='cart-detail'),
    path('check/', ShoppingCartCheckAllView.as_view(), name='cart-check-all'),
    path('clear/', ShoppingCartClearView.as_view(), name='cart-clear'),
]
