from django.core.management.base import BaseCommand
from apps.goods.models import GoodsCategory, Goods, GoodsSpec, GoodsParam
from apps.goods.ecommerce_factories import (
    EcommerceCategoryFactory, 
    EcommerceGoodsFactory, 
    EcommerceSpecFactory, 
    EcommerceParamFactory
)
import random

class Command(BaseCommand):
    help = '生成专业电商测试数据（包含分类、规格、参数）'

    def add_arguments(self, parser):
        parser.add_argument('--number', '-n', type=int, default=200, help='要生成的商品数量')
        parser.add_argument('--clear', action='store_true', help='清除现有数据')
        parser.add_argument('--with-specs', action='store_true', default=True, help='同时生成商品规格')
        parser.add_argument('--with-params', action='store_true', default=True, help='同时生成商品参数')
        parser.add_argument('--categories-only', action='store_true', help='只生成分类数据')
        parser.add_argument('--realistic', action='store_true', help='生成更真实的数据（销量和库存）')

    def handle(self, *args, **options):
        number = options['number']
        clear = options.get('clear')
        with_specs = options.get('with_specs')
        with_params = options.get('with_params')
        categories_only = options.get('categories_only')
        realistic = options.get('realistic')

        if clear:
            self.clear_data()
            self.stdout.write(self.style.SUCCESS('电商数据已清除'))

        # 创建电商分类体系
        self.stdout.write('正在创建电商分类体系...')
        categories = EcommerceCategoryFactory.create_ecommerce_categories()
        self.stdout.write(self.style.SUCCESS(f'创建了 {len(categories)} 个电商分类'))
        
        if categories_only:
            return

        self.stdout.write(f'开始生成 {number} 个专业电商商品数据...')

        created_goods = []
        category_stats = {}  # 统计每个分类的商品数量
        
        for i in range(number):
            try:
                # 使用电商工厂创建商品
                goods = EcommerceGoodsFactory.create()
                created_goods.append(goods)
                
                # 统计分类
                category_name = goods.category.category_name
                category_stats[category_name] = category_stats.get(category_name, 0) + 1
                
                # 生成规格和参数
                if with_specs:
                    self.create_ecommerce_specs(goods)
                
                if with_params:
                    self.create_ecommerce_params(goods)
                
                # 真实数据模式
                if realistic:
                    self.add_realistic_data(goods, category_name)
                
                if (i + 1) % 20 == 0:
                    self.stdout.write(f'已生成 {i + 1} 个商品...')

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'生成商品时出错: {e}'))
                continue

        # 输出统计信息
        self.stdout.write(self.style.SUCCESS(
            f'成功生成 {len(created_goods)} 个电商商品测试数据'
        ))
        
        if category_stats:
            self.stdout.write('\\n📊 分类商品分布:')
            for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
                self.stdout.write(f'  {category}: {count} 个商品')

    def clear_data(self):
        """清除现有数据"""
        GoodsParam.objects.all().delete()
        GoodsSpec.objects.all().delete()
        Goods.objects.all().delete()
        GoodsCategory.objects.all().delete()

    def create_ecommerce_specs(self, goods):
        """创建电商商品规格"""
        # 根据商品类型生成合适数量的规格
        category_name = goods.category.category_name
        num_specs = self.get_spec_count(category_name)
        
        for _ in range(num_specs):
            try:
                EcommerceSpecFactory.create(goods=goods)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'创建规格失败: {e}'))

    def create_ecommerce_params(self, goods):
        """创建电商商品参数"""
        # 根据商品类型生成合适数量的参数
        category_name = goods.category.category_name
        num_params = self.get_param_count(category_name)
        
        for _ in range(num_params):
            try:
                EcommerceParamFactory.create(goods=goods)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'创建参数失败: {e}'))

    def get_spec_count(self, category_name):
        """根据分类返回合适的规格数量"""
        if '手机' in category_name:
            return random.randint(3, 4)
        elif '电脑' in category_name or '笔记本' in category_name:
            return random.randint(4, 5)
        elif '服装' in category_name or '鞋' in category_name:
            return random.randint(2, 3)
        elif '家电' in category_name or '空调' in category_name:
            return random.randint(3, 4)
        elif '护肤' in category_name or '美妆' in category_name:
            return random.randint(2, 3)
        else:
            return random.randint(2, 4)

    def get_param_count(self, category_name):
        """根据分类返回合适的参数数量"""
        if '手机' in category_name:
            return random.randint(6, 8)
        elif '电脑' in category_name or '笔记本' in category_name:
            return random.randint(5, 7)
        elif '家电' in category_name:
            return random.randint(4, 6)
        elif '服装' in category_name:
            return random.randint(3, 5)
        elif '护肤' in category_name:
            return random.randint(4, 6)
        else:
            return random.randint(3, 6)

    def add_realistic_data(self, goods, category_name):
        """添加真实的数据模式"""
        # 根据商品价格和类型生成真实的销量和库存
        base_price = float(goods.goods_price)
        
        # 销量逻辑：价格适中、热门商品销量高
        if category_name in ['智能手机', '笔记本电脑', '运动鞋', '护肤品']:
            # 热门品类
            sales_weight = 0.8 if base_price < 5000 else 0.5
            if random.random() < sales_weight:
                goods.goods_sales = random.randint(500, 8000)
            else:
                goods.goods_sales = random.randint(50, 500)
        else:
            # 普通品类
            goods.goods_sales = random.randint(10, 1000)
        
        # 库存逻辑：高销量商品库存高，但也有热销缺货情况
        if goods.goods_sales > 2000:
            # 热销商品
            if random.random() < 0.8:  # 80%概率有充足库存
                goods.goods_stock = random.randint(100, 2000)
            else:  # 20%概率缺货或库存紧张
                goods.goods_stock = random.randint(0, 50)
        elif goods.goods_sales > 500:
            # 中等销量
            goods.goods_stock = random.randint(50, 500)
        else:
            # 低销量
            goods.goods_stock = random.randint(20, 200)
        
        goods.save()