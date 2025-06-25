
from django.urls import path
from .views import (
    OrderView,
    OrderDetailView,
    OrderCancelView,
    OrderConfirmView
)

urlpatterns = [
    path('', OrderView.as_view(), name='order-list'),
    path('<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:order_id>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
    path('<int:order_id>/confirm/', OrderConfirmView.as_view(), name='order-confirm'),
]