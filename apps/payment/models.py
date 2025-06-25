from django.db import models
from apps.orders.models import Order

class PaymentInfo(models.Model):
    """
    支付信息表
    """
    PAYMENT_STATUS_CHOICES = (
        (0, '未支付'),
        (1, '已支付')
    )
    
    PAYMENT_TYPE_CHOICES = (
        (1, '支付宝'),
        (2, '微信')
    )
    
    payment_id = models.AutoField(primary_key=True, verbose_name='支付ID')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='payments', verbose_name='订单')
    order_no = models.CharField(max_length=64, verbose_name='订单编号')
    payment_type = models.SmallIntegerField(choices=PAYMENT_TYPE_CHOICES, verbose_name='支付方式')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='交易流水号')
    payment_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='支付金额')
    payment_status = models.SmallIntegerField(choices=PAYMENT_STATUS_CHOICES, default=0, verbose_name='支付状态')
    payment_time = models.DateTimeField(blank=True, null=True, verbose_name='支付时间')
    callback_content = models.TextField(blank=True, null=True, verbose_name='回调内容')
    callback_time = models.DateTimeField(blank=True, null=True, verbose_name='回调时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        app_label = 'payment'
        db_table = 'payment_info'
        verbose_name = '支付信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return {
            'payment_id': self.payment_id,
            'order_id': self.order_id,
            'order_no': self.order_no,
            'payment_type': self.payment_type,
            'payment_status': self.payment_status,
            'payment_amount': float(self.payment_amount),
            'payment_time': self.payment_time.strftime('%Y-%m-%d %H:%M:%S') if self.payment_time else None
        }.__str__()
