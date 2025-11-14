from django.core.management.base import BaseCommand
from apps.orders.models import Order

class Command(BaseCommand):
    help = '设置指定订单的状态'

    def add_arguments(self, parser):
        parser.add_argument(
            'order_id',
            type=int,
            help='订单ID'
        )
        parser.add_argument(
            'status',
            type=int,
            choices=[0, 1, 2, 3, 4],
            help='订单状态 (0-已取消, 1-待付款, 2-待发货, 3-待收货, 4-已完成)'
        )

    def handle(self, *args, **options):
        order_id = options['order_id']
        status = options['status']
        
        try:
            order = Order.objects.get(order_id=order_id)
            old_status = order.order_status
            order.order_status = status
            order.save()
            
            old_status_name = dict(Order.ORDER_STATUS_CHOICES)[old_status]
            new_status_name = dict(Order.ORDER_STATUS_CHOICES)[status]
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'订单{order_id}状态已从 {old_status_name}({old_status}) 改为 {new_status_name}({status})'
                )
            )
        except Order.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'订单{order_id}不存在')
            )
