from django.db import models
from apps.accounts.models import User
from apps.goods.models import Goods

class ShoppingCart(models.Model):
    """
    购物车表
    """
    cart_id = models.AutoField(primary_key=True, verbose_name='购物车ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', verbose_name='用户')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    goods_num = models.PositiveIntegerField(default=1, verbose_name='商品数量')
    selected = models.BooleanField(default=True, verbose_name='是否选中')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        app_label = 'cart'
        db_table = 'shopping_cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'goods')  # 用户和商品的唯一组合

    def __str__(self):
        return f"购物车项: 用户{self.user.username} - 商品{self.goods.goods_name} x {self.goods_num}"

    def clean(self):
        # 模型验证
        from django.core.exceptions import ValidationError
        if not self.user_id:
            raise ValidationError("用户信息不能为空")
        if not self.goods_id:
            raise ValidationError("商品信息不能为空")
        if self.goods_num <= 0:
            raise ValidationError("商品数量必须大于0")