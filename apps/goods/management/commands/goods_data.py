from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.goods.models import GoodsCategory, Goods, GoodsSpec, GoodsParam
from apps.goods.factories import GoodsCategoryFactory, GoodsFactory, GoodsSpecFactory, GoodsParamFactory
import random

class Command(BaseCommand):
    help = '使用factory_boy生成商品测试数据（包含分类、规格、参数）'

    def add_arguments(self, parser):
        parser.add_argument('--number', '-n', type=int, default=150, help='要生成的商品数量')
        parser.add_argument('--clear', action='store_true', help='清除现有商品数据')
        parser.add_argument('--with-specs', action='store_true', help='同时生成商品规格')
        parser.add_argument('--with-params', action='store_true', help='同时生成商品参数')
        parser.add_argument('--categories-only', action='store_true', help='只生成分类数据')

    def handle(self, *args, **options):
        number = options['number']
        clear = options.get('clear')
        with_specs = options.get('with_specs')
        with_params = options.get('with_params')
        categories_only = options.get('categories_only')

        if clear:
            self.clear_data()
            self.stdout.write(self.style.SUCCESS('商品数据已清除'))

        # 创建商品分类
        self.create_categories()
        
        if categories_only:
            self.stdout.write(self.style.SUCCESS('商品分类创建完成'))
            return

        self.stdout.write(f'开始生成 {number} 个商品测试数据...')

        created_goods = []
        for i in range(number):
            try:
                # 使用factory_boy创建商品
                goods = GoodsFactory.create()
                created_goods.append(goods)
                
                if with_specs:
                    self.create_goods_specs(goods)
                
                if with_params:
                    self.create_goods_params(goods)
                
                if (i + 1) % 20 == 0:
                    self.stdout.write(f'已生成 {i + 1} 个商品...')

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'生成商品时出错: {e}'))
                continue

        self.stdout.write(self.style.SUCCESS(
            f'成功生成 {len(created_goods)} 个商品测试数据'
        ))

    def clear_data(self):
        """清除现有数据"""
        # 按依赖关系顺序删除，避免外键约束问题
        GoodsParam.objects.all().delete()
        GoodsSpec.objects.all().delete()
        GoodsCategory.objects.all().delete()
        
        # 注意：商品不能直接删除，因为被订单项引用
        # 如果需要重新生成商品，建议先删除相关订单数据
        # 这里只是清除规格、参数和分类
        self.stdout.write(self.style.WARNING('商品数据未被清除，因为存在订单依赖。如需重新生成，请先清理订单数据。'))

    def create_categories(self):
        """创建商品分类"""
        # 一级分类
        main_categories_data = [
            {'name': '手机数码', 'icon': '📱', 'children': ['智能手机', '平板电脑', '智能手表', '耳机音箱']},
            {'name': '电脑办公', 'icon': '💻', 'children': ['笔记本电脑', '台式电脑', '办公设备', '电脑配件']},
            {'name': '家用电器', 'icon': '🏠', 'children': ['大家电', '厨房电器', '生活电器', '个人护理']},
            {'name': '服装鞋帽', 'icon': '👕', 'children': ['男装', '女装', '童装', '鞋类']},
            {'name': '美妆个护', 'icon': '💄', 'children': ['护肤', '彩妆', '香水', '美发']},
            {'name': '食品生鲜', 'icon': '🍎', 'children': ['休闲食品', '生鲜果蔬', '酒水饮料', '粮油调味']},
            {'name': '运动户外', 'icon': '⚽', 'children': ['运动鞋服', '体育器材', '户外装备', '健身器材']},
            {'name': '家居家装', 'icon': '🛋️', 'children': ['家具', '家纺', '家居装饰', '厨房用品']},
            {'name': '母婴玩具', 'icon': '🧸', 'children': ['奶粉辅食', '母婴用品', '童装童鞋', '玩具']},
            {'name': '图书文具', 'icon': '📚', 'children': ['图书', '文具', '办公用品', '电子书']}
        ]

        created_categories = []
        for i, cat_data in enumerate(main_categories_data):
            # 创建一级分类
            main_category = GoodsCategory.objects.create(
                category_name=cat_data['name'],
                category_level=1,
                category_icon=cat_data['icon'],
                sort_order=i * 10,
                status=True
            )
            created_categories.append(main_category)
            
            # 创建二级分类
            for j, child_name in enumerate(cat_data['children']):
                sub_category = GoodsCategory.objects.create(
                    category_name=child_name,
                    parent=main_category,
                    category_level=2,
                    sort_order=j * 5,
                    status=True
                )
                created_categories.append(sub_category)

        self.stdout.write(self.style.SUCCESS(f'创建了 {len(created_categories)} 个商品分类'))
        return created_categories

    def create_goods_specs(self, goods):
        """创建商品规格"""
        # 每个商品生成2-4个规格
        num_specs = random.randint(2, 4)
        
        for _ in range(num_specs):
            try:
                GoodsSpecFactory.create(goods=goods)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'创建规格失败: {e}'))

    def create_goods_params(self, goods):
        """创建商品参数"""
        # 每个商品生成3-6个参数
        num_params = random.randint(3, 6)
        
        for _ in range(num_params):
            try:
                GoodsParamFactory.create(goods=goods)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'创建参数失败: {e}'))