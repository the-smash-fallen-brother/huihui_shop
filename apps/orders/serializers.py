
from rest_framework import serializers
from .models import Order, OrderItem
from apps.goods.models import Goods

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['item_id', 'order', 'goods', 'goods_name', 'goods_cover_img',
                 'goods_price', 'goods_num', 'goods_total_price', 'create_time']
        extra_kwargs = {
            'item_id': {'read_only': True},
            'create_time': {'read_only': True}
        }

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    order_status_text = serializers.CharField(source='get_order_status_display', read_only=True)
    payment_type_text = serializers.CharField(source='get_payment_type_display', read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'order_no', 'user', 'total_amount', 'payment_amount',
                 'shipping_fee', 'payment_type', 'order_status', 'order_status_text', 
                 'payment_type_text', 'payment_time', 'shipping_time', 'completion_time', 
                 'receiver_name', 'receiver_mobile', 'receiver_address', 'remark', 
                 'items', 'create_time', 'update_time']
        extra_kwargs = {
            'order_id': {'read_only': True},
            'order_no': {'read_only': True},
            'user': {'read_only': True},
            'create_time': {'read_only': True},
            'update_time': {'read_only': True}
        }

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address_info = serializers.SerializerMethodField()
    order_status_text = serializers.CharField(source='get_order_status_display', read_only=True)
    payment_type_text = serializers.CharField(source='get_payment_type_display', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_address_info(self, obj):
        return {
            'receiver_name': obj.receiver_name,
            'receiver_mobile': obj.receiver_mobile,
            'receiver_address': obj.receiver_address
        }