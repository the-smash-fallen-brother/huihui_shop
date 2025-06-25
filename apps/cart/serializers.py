
from rest_framework import serializers
from .models import ShoppingCart
from apps.goods.models import Goods

class ShoppingCartSerializer(serializers.ModelSerializer):
    goods_info = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ['cart_id', 'user', 'goods', 'goods_num', 'selected', 'goods_info', 'create_time', 'update_time']
        extra_kwargs = {
            'user': {'read_only': True},
            'cart_id': {'read_only': True},
            'create_time': {'read_only': True},
            'update_time': {'read_only': True}
        }

    def get_goods_info(self, obj):
        goods = obj.goods
        return {
            'goods_id': goods.goods_id,
            'goods_name': goods.goods_name,
            'goods_price': str(goods.goods_price),
            'goods_cover_img': goods.goods_cover_img,
            'goods_stock': goods.goods_stock
        }

class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'