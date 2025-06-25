from django.urls import path
from .views import PaymentView

urlpatterns = [
    # 支付相关路由
    path('orders/<int:order_id>/payment/', PaymentView.as_view(), name='payment-info'),
    path('orders/<int:order_id>/pay/', PaymentView.as_view(), name='payment-process'),
]