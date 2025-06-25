
from rest_framework import serializers
from .models import PaymentInfo
from apps.orders.models import Order

class PaymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInfo
        fields = ['payment_id', 'order', 'order_no', 'payment_type',
                 'transaction_id', 'payment_amount', 'payment_status',
                 'payment_time', 'callback_content', 'callback_time',
                 'create_time', 'update_time']
        extra_kwargs = {
            'payment_id': {'read_only': True},
            'create_time': {'read_only': True},
            'update_time': {'read_only': True}
        }