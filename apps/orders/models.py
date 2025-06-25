from django.db import models
from apps.accounts.models import User
from apps.goods.models import Goods

class Order(models.Model):
    """
    订单主表
    """
    ORDER_STATUS_CHOICES = (
        (0, '已取消'),
        (1, '待付款'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '已完成')
    )
    
    PAYMENT_TYPE_CHOICES = (
        (1, '支付宝'),
        (2, '微信')
    )
    
    order_id = models.AutoField(primary_key=True, verbose_name='订单ID')
    order_no = models.CharField(max_length=64, unique=True, verbose_name='订单编号')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders', verbose_name='用户')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='订单总金额')
    payment_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='实付金额')
    shipping_fee = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='运费')
    payment_type = models.SmallIntegerField(choices=PAYMENT_TYPE_CHOICES, null=True, blank=True, verbose_name='支付方式')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    payment_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    shipping_time = models.DateTimeField(null=True, blank=True, verbose_name='发货时间')
    completion_time = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    receiver_name = models.CharField(max_length=50, verbose_name='收货人姓名')
    receiver_mobile = models.CharField(max_length=11, verbose_name='收货人手机号')
    receiver_address = models.CharField(max_length=255, verbose_name='收货地址')
    remark = models.CharField(max_length=500, blank=True, null=True, verbose_name='订单备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        app_label = 'orders'
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return {
            'order_id': self.order_id,
            'order_no': self.order_no,
            'user_id': self.user_id,
            'total_amount': float(self.total_amount),
            'payment_amount': float(self.payment_amount),
            'order_status': self.order_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }.__str__()


class OrderItem(models.Model):
    """
    订单项表
    """
    item_id = models.AutoField(primary_key=True, verbose_name='订单项ID')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    goods = models.ForeignKey(Goods, on_delete=models.PROTECT, verbose_name='商品')
    goods_name = models.CharField(max_length=100, verbose_name='商品名称')
    goods_cover_img = models.URLField(max_length=255, verbose_name='商品封面图')
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品单价')
    goods_num = models.PositiveIntegerField(verbose_name='商品数量')
    goods_total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总价')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        app_label = 'orders'
        db_table = 'order_item'
        verbose_name = '订单项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return {
            'item_id': self.item_id,
            'order_id': self.order_id,
            'goods_id': self.goods_id,
            'goods_name': self.goods_name,
            'goods_price': float(self.goods_price),
            'goods_num': self.goods_num,
            'goods_total_price': float(self.goods_total_price)
        }.__str__()
