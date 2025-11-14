from rest_framework import serializers
from .models import ShoppingCart
from apps.goods.models import Goods
import logging

logger = logging.getLogger(__name__)


class ShoppingCartSerializer(serializers.ModelSerializer):
    goods_info = serializers.SerializerMethodField()
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all())

    class Meta:
        model = ShoppingCart
        fields = ['cart_id', 'user', 'goods', 'goods_num', 'selected', 'goods_info', 'create_time', 'update_time']
        read_only_fields = ['user', 'cart_id', 'create_time', 'update_time']

    def get_goods_info(self, obj):
        goods = obj.goods
        return {
            'goods_id': goods.goods_id,
            'goods_name': goods.goods_name,
            'goods_price': str(goods.goods_price),
            'goods_cover_img': goods.goods_cover_img,
            'goods_stock': goods.goods_stock
        }

    def validate_user(self, value):
        # 验证用户字段，确保与请求用户一致
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user != value:
            raise serializers.ValidationError("用户信息不匹配")
        return value

    def validate_goods_num(self, value):
        # 验证商品数量
        if value <= 0:
            raise serializers.ValidationError("商品数量必须大于0")
        return value

    def validate(self, attrs):
        # 整体验证
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError("无法获取用户信息")
        
        # 设置用户为当前认证用户
        attrs['user'] = request.user
        
        # 在创建时检查商品信息，更新时不需要检查（因为商品信息来自现有实例）
        if not self.instance:  # 创建新实例时
            goods = attrs.get('goods')
            if not goods:
                raise serializers.ValidationError("商品信息不能为空")
            
            # 检查商品库存
            if goods.goods_stock <= 0:
                raise serializers.ValidationError("商品库存不足")
                
            goods_num = attrs.get('goods_num', 1)
            if goods_num > goods.goods_stock:
                raise serializers.ValidationError("商品数量不能超过库存")
        else:  # 更新现有实例时
            goods = self.instance.goods
            goods_num = attrs.get('goods_num', 1)
            
            # 检查商品是否上架
            if hasattr(goods, 'goods_status') and goods.goods_status != 1:
                raise serializers.ValidationError("商品已下架，无法更新数量")
            
            # 检查库存是否充足
            if goods_num > goods.goods_stock:
                raise serializers.ValidationError(f"商品数量({goods_num})不能超过库存({goods.goods_stock})")
            if goods.goods_stock <= 0:
                raise serializers.ValidationError("商品库存不足")
            if goods_num <= 0:
                raise serializers.ValidationError("商品数量必须大于0")
        
        return attrs

    # def validate(self, attrs):
    #     # 整体验证
    #     request = self.context.get('request')
    #     if not request or not hasattr(request, 'user'):
    #         raise serializers.ValidationError("无法获取用户信息")
        
    #     # 设置用户为当前认证用户
    #     attrs['user'] = request.user
        
    #     # 在创建时检查商品信息
    #     if not self.instance:  # 创建新实例时
    #         goods_id = attrs.get('goods')
    #     if not goods_id:
    #         raise serializers.ValidationError("商品信息不能为空")
        
    #     # 获取商品对象进行验证
    #     try:
    #         goods_obj = Goods.objects.get(id=goods_id)
    #     except Goods.DoesNotExist:
    #         raise serializers.ValidationError("商品不存在")
        
    #     # 使用商品对象进行库存验证
    #     if goods_obj.goods_stock <= 0:
    #         raise serializers.ValidationError("商品库存不足")
            
    #     goods_num = attrs.get('goods_num', 1)
    #     if goods_num > goods_obj.goods_stock:
    #         raise serializers.ValidationError("商品数量不能超过库存")
            
    #     else:  # 更新现有实例时
    #     # 更新时 goods 已经是对象了
    #         goods_obj = self.instance.goods
    #         goods_num = attrs.get('goods_num', self.instance.goods_num)
        
    #     # 检查商品是否上架
    #     if hasattr(goods_obj, 'goods_status') and goods_obj.goods_status != 1:
    #         raise serializers.ValidationError("商品已下架，无法更新数量")
        
    #     # 检查库存是否充足
    #     if goods_num > goods_obj.goods_stock:
    #         raise serializers.ValidationError(f"商品数量({goods_num})不能超过库存({goods_obj.goods_stock})")
    #     if goods_obj.goods_stock <= 0:
    #         raise serializers.ValidationError("商品库存不足")
    #     if goods_num <= 0:
    #         raise serializers.ValidationError("商品数量必须大于0")
    
    #     return attrs
    # def validate(self, attrs):
    #     request = self.context.get('request')
    #     if not request or not request.user.is_authenticated:
    #         raise serializers.ValidationError({'user': '用户未认证或登录失效'})

    #         attrs['user'] = request.user

    #     if not self.instance:  # 创建
    #         goods = attrs.get('goods')
    #         if not goods:
    #             raise serializers.ValidationError({'goods': '商品信息不能为空'})

    #         if goods.goods_stock <= 0:
    #             raise serializers.ValidationError({'goods': '该商品暂无库存'})
        
    #         goods_num = attrs.get('goods_num', 1)
    #         if goods_num > goods.goods_stock:
    #             raise serializers.ValidationError({
    #             'goods_num': f'购买数量不能超过库存 {goods.goods_stock}'
    #         })

    #     else:  # 更新
    #         old_goods = self.instance.goods
    #         new_goods_num = attrs.get('goods_num', self.instance.goods_num)

    #         if hasattr(old_goods, 'goods_status') and old_goods.goods_status != 1:
    #             raise serializers.ValidationError({'goods': '商品已下架，无法修改'})

    #         if new_goods_num > old_goods.goods_stock:
    #             raise serializers.ValidationError({
    #             'goods_num': f'数量超出库存限制（当前库存：{old_goods.goods_stock}）'
    #         })
    #         if new_goods_num <= 0:
    #             raise serializers.ValidationError({'goods_num': '数量必须大于0'})

    #     return attrs

class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'
        read_only_fields = ['user', 'cart_id', 'goods', 'create_time', 'update_time']
        
    def validate_goods_num(self, value):
        # 验证商品数量
        logger.info(f"验证商品数量: {value}")
        if value <= 0:
            raise serializers.ValidationError("商品数量必须大于0")
        return value
        
    def validate(self, attrs):
        # 更新时的验证
        logger.info(f"开始更新验证: attrs={attrs}")
        
        if 'user' in attrs:
            # 不允许更新用户字段
            logger.warning("尝试更新用户字段，已移除")
            del attrs['user']
            
        goods = attrs.get('goods')
        if goods and hasattr(goods, 'goods_stock'):
            goods_num = attrs.get('goods_num', 1)
            logger.info(f"验证商品: goods_id={getattr(goods, 'goods_id', 'unknown')}, goods_num={goods_num}, goods_stock={goods.goods_stock}")
            
            # 检查商品是否上架
            if hasattr(goods, 'goods_status') and goods.goods_status != 1:
                logger.warning(f"商品已下架: goods_status={goods.goods_status}")
                raise serializers.ValidationError("商品已下架，无法更新数量")
            
            # 检查库存是否充足
            if goods_num > goods.goods_stock:
                logger.warning(f"商品数量超过库存: goods_num={goods_num}, goods_stock={goods.goods_stock}")
                raise serializers.ValidationError(f"商品数量({goods_num})不能超过库存({goods.goods_stock})")
            if goods.goods_stock <= 0:
                logger.warning(f"商品库存不足: goods_stock={goods.goods_stock}")
                raise serializers.ValidationError("商品库存不足")
            if goods_num <= 0:
                logger.warning(f"商品数量必须大于0: goods_num={goods_num}")
                raise serializers.ValidationError("商品数量必须大于0")
                
        logger.info("更新验证通过")
        return attrs
