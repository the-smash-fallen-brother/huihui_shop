from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.orders.models import Order
import random

class Command(BaseCommand):
    help = '模拟订单完成状态，将指定时间前的订单状态改为已完成'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=3,
            help='将多少天前的订单设为已完成（默认3天）'
        )
        parser.add_argument(
            '--hours',
            type=int,
            default=0,
            help='将多少小时前的订单设为已完成（默认0小时）'
        )
        parser.add_argument(
            '--status',
            type=int,
            choices=[1, 2, 3],
            default=3,
            help='只处理指定状态的订单（1-待付款，2-待发货，3-待收货，默认3）'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='最多处理多少个订单（默认10个）'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='只显示将要处理的订单，不实际修改'
        )

    def handle(self, *args, **options):
        days = options['days']
        hours = options['hours']
        status = options['status']
        limit = options['limit']
        dry_run = options['dry_run']

        # 计算时间阈值
        time_threshold = timezone.now() - timedelta(days=days, hours=hours)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'查找 {time_threshold.strftime("%Y-%m-%d %H:%M:%S")} 之前状态为 {status} 的订单...'
            )
        )

        # 查找符合条件的订单
        orders = Order.objects.filter(
            order_status=status,
            create_time__lt=time_threshold
        ).order_by('create_time')[:limit]

        if not orders.exists():
            self.stdout.write(
                self.style.WARNING('没有找到符合条件的订单')
            )
            return

        self.stdout.write(f'找到 {orders.count()} 个符合条件的订单:')

        # 显示订单信息
        for order in orders:
            status_text = dict(Order.ORDER_STATUS_CHOICES)[order.order_status]
            self.stdout.write(
                f'  订单ID: {order.order_id}, '
                f'订单号: {order.order_no}, '
                f'状态: {status_text}, '
                f'创建时间: {order.create_time.strftime("%Y-%m-%d %H:%M:%S")}, '
                f'金额: ¥{order.total_amount}'
            )

        if dry_run:
            self.stdout.write(
                self.style.WARNING('这是试运行模式，没有实际修改订单状态')
            )
            return

        # 确认操作
        confirm = input(f'\n确认要将这 {orders.count()} 个订单状态改为已完成吗？(y/N): ')
        if confirm.lower() != 'y':
            self.stdout.write('操作已取消')
            return

        # 更新订单状态
        updated_count = 0
        for order in orders:
            # 模拟订单流程：设置支付时间、发货时间、完成时间
            if order.order_status == 1:
                # 待付款 -> 已完成
                order.payment_time = order.create_time + timedelta(hours=1)
                order.shipping_time = order.create_time + timedelta(hours=2)
                order.completion_time = order.create_time + timedelta(days=1)
            elif order.order_status == 2:
                # 待发货 -> 已完成
                order.shipping_time = order.create_time + timedelta(hours=1)
                order.completion_time = order.create_time + timedelta(days=1)
            elif order.order_status == 3:
                # 待收货 -> 已完成
                order.completion_time = order.create_time + timedelta(days=1)
            
            order.order_status = 4  # 已完成
            order.save()
            updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'成功将 {updated_count} 个订单状态更新为已完成'
            )
        )

        # 显示更新后的订单状态
        self.stdout.write('\n更新后的订单状态:')
        for order in orders:
            self.stdout.write(
                f'  订单ID: {order.order_id}, '
                f'状态: 已完成, '
                f'完成时间: {order.completion_time.strftime("%Y-%m-%d %H:%M:%S")}'
            )
