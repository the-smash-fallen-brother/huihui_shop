from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.goods.models import Goods
import random

class Command(BaseCommand):
    help = '创建秒杀商品测试数据'

    def add_arguments(self, parser):
        parser.add_argument('--number', '-n', type=int, default=5, help='要设置的商品数量')
        parser.add_argument('--clear', action='store_true', help='清除所有秒杀设置')

    def handle(self, *args, **options):
        number = options['number']
        clear = options.get('clear')

        if clear:
            self.clear_flash_sale_data()
            self.stdout.write(self.style.SUCCESS('秒杀设置已清除'))

        self.create_flash_sale_goods(number)

    def clear_flash_sale_data(self):
        """清除所有秒杀设置"""
        Goods.objects.all().update(
            is_flash_sale=False,
            flash_sale_price=None,
            flash_sale_stock=0,
            flash_sale_start_time=None,
            flash_sale_end_time=None
        )

    def create_flash_sale_goods(self, number):
        """创建秒杀商品"""
        current_time = timezone.now()
        
        # 获取一些普通商品来设置为秒杀商品
        regular_goods = Goods.objects.filter(
            is_flash_sale=False,
            goods_status=1
        )[:number]

        if not regular_goods.exists():
            self.stdout.write(self.style.WARNING('没有找到可用的普通商品，请先创建商品'))
            return

        created_count = 0
        for goods in regular_goods:
            try:
                # 设置秒杀价格（原价的3-7折）
                discount_rate = random.uniform(0.3, 0.7)
                flash_sale_price = goods.goods_price * discount_rate
                
                # 设置秒杀库存（总库存的10-30%）
                flash_sale_stock = max(1, int(goods.goods_stock * random.uniform(0.1, 0.3)))
                
                # 随机设置秒杀时间段
                start_time_options = [
                    current_time - timedelta(hours=random.randint(1, 6)),  # 已经开始的
                    current_time + timedelta(minutes=random.randint(10, 120)),  # 即将开始的
                ]
                
                start_time = random.choice(start_time_options)
                duration_hours = random.randint(2, 8)
                end_time = start_time + timedelta(hours=duration_hours)
                
                # 更新商品为秒杀商品
                goods.is_flash_sale = True
                goods.flash_sale_price = flash_sale_price
                goods.flash_sale_stock = flash_sale_stock
                goods.flash_sale_start_time = start_time
                goods.flash_sale_end_time = end_time
                goods.save()
                
                created_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'已设置秒杀商品: {goods.goods_name} - '
                        f'原价: ¥{goods.goods_price} -> 秒杀价: ¥{flash_sale_price:.2f} - '
                        f'库存: {flash_sale_stock} - '
                        f'时间: {start_time.strftime("%Y-%m-%d %H:%M")} 至 {end_time.strftime("%Y-%m-%d %H:%M")}'
                    )
                )
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'设置秒杀商品失败 {goods.goods_name}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'成功设置了 {created_count} 个秒杀商品'))
