import os
import django
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from apps.cart.models import ShoppingCart
from apps.cart.serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer
from apps.goods.models import Goods
from apps.accounts.models import User

# 模拟测试数据
def test_cart_update():
    # 获取用户和商品
    user = User.objects.first()
    goods = Goods.objects.first()
    
    if not user or not goods:
        print("没有找到用户或商品")
        return
    
    # 创建购物车项
    cart_item = ShoppingCart.objects.create(
        user=user,
        goods=goods,
        goods_num=1,
        selected=True
    )
    
    print(f"创建购物车项: {cart_item}")
    
    # 测试更新数据
    update_data = {
        'goods_num': 2,
        'selected': True
    }
    
    print(f"更新数据: {update_data}")
    
    # 使用序列化器验证
    serializer = ShoppingCartDetailSerializer(cart_item, data=update_data)
    is_valid = serializer.is_valid()
    
    print(f"序列化器验证结果: {is_valid}")
    if not is_valid:
        print(f"验证错误: {serializer.errors}")
    else:
        updated_item = serializer.save()
        print(f"更新后的购物车项: {updated_item}")
        
    # 清理测试数据
    cart_item.delete()

if __name__ == "__main__":
    test_cart_update()