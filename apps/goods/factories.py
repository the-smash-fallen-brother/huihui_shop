import factory
from factory import fuzzy
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
import random
from .models import GoodsCategory, Goods, GoodsSpec, GoodsParam

class GoodsCategoryFactory(factory.django.DjangoModelFactory):
    """商品分类工厂"""
    class Meta:
        model = GoodsCategory
    
    category_name = factory.Faker('word', locale='zh_CN')
    parent = None
    category_level = fuzzy.FuzzyChoice([1, 2])
    category_icon = factory.Faker('emoji')
    sort_order = fuzzy.FuzzyInteger(0, 100)
    status = True

class GoodsFactory(factory.django.DjangoModelFactory):
    """商品工厂"""
    class Meta:
        model = Goods
    
    goods_name = factory.Faker('catch_phrase', locale='zh_CN')
    goods_price = fuzzy.FuzzyDecimal(50.00, 5000.00, 2)
    goods_desc = factory.Faker('text', max_nb_chars=200, locale='zh_CN')
    goods_cover_img = factory.LazyAttributeSequence(
        lambda obj, n: f'https://picsum.photos/seed/goods{n}/800/800.jpg'
    )
    goods_carousel = factory.LazyAttributeSequence(
        lambda obj, n: [
            f'https://picsum.photos/seed/carousel{i}_{n}/800/800.jpg'
            for i in range(random.randint(3, 5))
        ]
    )
    goods_stock = fuzzy.FuzzyInteger(10, 1000)
    goods_sales = fuzzy.FuzzyInteger(0, 500)
    goods_status = factory.LazyFunction(lambda: random.choices([0, 1], weights=[1, 4])[0])
    create_time = factory.LazyFunction(
        lambda: timezone.now() - timedelta(days=random.randint(0, 365))
    )
    
    @factory.lazy_attribute
    def market_price(self):
        return self.goods_price * Decimal('1.2')
    
    @factory.lazy_attribute
    def cost_price(self):
        return self.goods_price * Decimal('0.7')
    
    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        """确保有分类"""
        if 'category' not in kwargs:
            # 获取或创建一个二级分类
            level2_categories = GoodsCategory.objects.filter(category_level=2)
            if not level2_categories.exists():
                # 如果没有二级分类，创建一个
                parent = GoodsCategoryFactory.create(category_level=1)
                kwargs['category'] = GoodsCategoryFactory.create(
                    parent=parent,
                    category_level=2
                )
            else:
                kwargs['category'] = random.choice(level2_categories)
        
        # 设置市场价格和成本价格
        if 'goods_price' in kwargs:
            base_price = kwargs['goods_price']
            kwargs.setdefault('market_price', base_price * Decimal('1.2'))
            kwargs.setdefault('cost_price', base_price * Decimal('0.7'))
        
        return kwargs

class GoodsSpecFactory(factory.django.DjangoModelFactory):
    """商品规格工厂"""
    class Meta:
        model = GoodsSpec
    
    spec_name = factory.Faker('word', locale='zh_CN')
    spec_value = factory.Faker('word', locale='zh_CN')
    
    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        """智能规格生成"""
        goods = kwargs.get('goods')
        if goods:
            category_name = goods.category.category_name
            
            # 根据商品分类智能选择规格
            spec_templates = {
                '手机': [
                    ('颜色', ['黑色', '白色', '银色', '蓝色', '红色']),
                    ('内存', ['8GB', '12GB', '16GB', '32GB']),
                    ('存储', ['128GB', '256GB', '512GB', '1TB']),
                ],
                '电脑': [
                    ('颜色', ['黑色', '白色', '银色']),
                    ('内存', ['8GB', '16GB', '32GB']),
                    ('硬盘', ['256GB SSD', '512GB SSD', '1TB SSD']),
                ],
                '服装': [
                    ('颜色', ['黑色', '白色', '灰色', '蓝色']),
                    ('尺码', ['S', 'M', 'L', 'XL']),
                    ('材质', ['纯棉', '涤纶', '尼龙']),
                ],
            }
            
            # 匹配分类
            for key in spec_templates:
                if key in category_name:
                    spec_data = random.choice(spec_templates[key])
                    kwargs['spec_name'] = spec_data[0]
                    kwargs['spec_value'] = random.choice(spec_data[1])
                    break
            else:
                # 默认规格
                kwargs['spec_name'] = random.choice(['颜色', '尺寸', '型号'])
                kwargs['spec_value'] = random.choice(['黑色', '标准', 'A型'])
        
        return kwargs

class GoodsParamFactory(factory.django.DjangoModelFactory):
    """商品参数工厂"""
    class Meta:
        model = GoodsParam
    
    param_name = factory.Faker('word', locale='zh_CN')
    param_value = factory.Faker('word', locale='zh_CN')
    
    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        """智能参数生成"""
        goods = kwargs.get('goods')
        if goods:
            category_name = goods.category.category_name
            
            # 根据商品分类智能选择参数
            param_templates = {
                '手机': [
                    ('品牌', ['苹果', '华为', '小米', '三星']),
                    ('型号', [f'MODEL-{random.randint(1000, 9999)}']),
                    ('屏幕尺寸', ['6.1英寸', '6.5英寸', '6.7英寸']),
                    ('处理器', ['A15', 'A16', 'A17']),
                ],
                '电脑': [
                    ('品牌', ['戴尔', '联想', '华为', '苹果']),
                    ('处理器', ['Intel i5', 'Intel i7', 'AMD Ryzen 5']),
                    ('内存', ['8GB', '16GB', '32GB']),
                    ('硬盘容量', ['256GB', '512GB', '1TB']),
                ],
                '服装': [
                    ('品牌', ['耐克', '阿迪达斯', '优衣库', 'ZARA']),
                    ('材质', ['纯棉', '涤纶', '尼龙', '羊毛']),
                    ('产地', ['中国', '越南', '孟加拉']),
                ],
            }
            
            # 匹配分类
            for key in param_templates:
                if key in category_name:
                    param_data = random.choice(param_templates[key])
                    kwargs['param_name'] = param_data[0]
                    if isinstance(param_data[1], list):
                        kwargs['param_value'] = random.choice(param_data[1])
                    else:
                        kwargs['param_value'] = param_data[1]
                    break
            else:
                # 默认参数
                kwargs['param_name'] = random.choice(['品牌', '型号', '产地'])
                kwargs['param_value'] = random.choice(['品牌A', 'MODEL-100', '中国'])
        
        return kwargs