# apps/goods/management/commands/generate_goods.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from decimal import Decimal
from faker import Faker
from apps.goods.models import GoodsCategory, Goods, GoodsSpec, GoodsParam

fake = Faker('zh_CN')

class Command(BaseCommand):
    help = '生成商品测试数据（包含分类、规格、参数）'

    def add_arguments(self, parser):
        parser.add_argument('--number', '-n', type=int, default=150, help='要生成的商品数量')
        parser.add_argument('--clear', action='store_true', help='清除现有商品数据')
        parser.add_argument('--with-specs', action='store_true', help='同时生成商品规格')
        parser.add_argument('--with-params', action='store_true', help='同时生成商品参数')

    def handle(self, *args, **options):
        number = options['number']
        clear = options.get('clear')
        with_specs = options.get('with_specs')
        with_params = options.get('with_params')

        if clear:
            GoodsParam.objects.all().delete()
            GoodsSpec.objects.all().delete()
            Goods.objects.all().delete()
            GoodsCategory.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('商品数据已清除'))

        # 首先创建商品分类
        categories = self.create_categories()
        
        self.stdout.write(f'开始生成 {number} 个商品测试数据...')

        created_goods = []
        for i in range(number):
            try:
                goods = self.create_goods(i, categories)
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

    def create_categories(self):
        """创建商品分类"""
        # 一级分类
        main_categories = [
            {'name': '手机数码', 'icon': '📱'},
            {'name': '电脑办公', 'icon': '💻'},
            {'name': '家用电器', 'icon': '🏠'},
            {'name': '服装鞋帽', 'icon': '👕'},
            {'name': '美妆个护', 'icon': '💄'},
            {'name': '食品生鲜', 'icon': '🍎'},
            {'name': '运动户外', 'icon': '⚽'},
            {'name': '家居家装', 'icon': '🛋️'},
            {'name': '母婴玩具', 'icon': '🧸'},
            {'name': '图书文具', 'icon': '📚'}
        ]

        categories = []
        for i, cat_data in enumerate(main_categories):
            category = GoodsCategory.objects.create(
                category_name=cat_data['name'],
                category_level=1,
                category_icon=cat_data['icon'],
                sort_order=i * 10,
                status=True
            )
            categories.append(category)
            
            # 为每个一级分类创建2-3个二级分类
            sub_categories = self.get_sub_categories(cat_data['name'])
            for j, sub_name in enumerate(sub_categories):
                sub_category = GoodsCategory.objects.create(
                    category_name=sub_name,
                    parent=category,
                    category_level=2,
                    sort_order=j * 5,
                    status=True
                )
                categories.append(sub_category)

        return categories

    def get_sub_categories(self, main_category):
        """根据一级分类获取二级分类"""
        sub_categories_map = {
            '手机数码': ['智能手机', '平板电脑', '智能手表', '耳机音箱'],
            '电脑办公': ['笔记本电脑', '台式电脑', '办公设备', '电脑配件'],
            '家用电器': ['大家电', '厨房电器', '生活电器', '个人护理'],
            '服装鞋帽': ['男装', '女装', '童装', '鞋类'],
            '美妆个护': ['护肤', '彩妆', '香水', '美发'],
            '食品生鲜': ['休闲食品', '生鲜果蔬', '酒水饮料', '粮油调味'],
            '运动户外': ['运动鞋服', '体育器材', '户外装备', '健身器材'],
            '家居家装': ['家具', '家纺', '家居装饰', '厨房用品'],
            '母婴玩具': ['奶粉辅食', '母婴用品', '童装童鞋', '玩具'],
            '图书文具': ['图书', '文具', '办公用品', '电子书']
        }
        return sub_categories_map.get(main_category, ['默认分类'])

    def create_goods(self, index, categories):
        """创建单个商品"""
        # 选择二级分类
        level2_categories = [cat for cat in categories if cat.category_level == 2]
        if not level2_categories:
            # 如果没有二级分类，使用一级分类
            level2_categories = [cat for cat in categories if cat.category_level == 1]
        
        category = random.choice(level2_categories)
        
        # 商品名称和描述
        goods_name = self.generate_goods_name(category.category_name)
        goods_desc = self.generate_goods_description(goods_name)
        
        # 价格计算
        base_price = Decimal(str(round(random.uniform(50, 5000), 2)))
        market_price = base_price * Decimal('1.2')  # 市场价格比基础价高20%
        cost_price = base_price * Decimal('0.7')    # 成本价比基础价低30%
        
        # 生成商品图片URL - 使用Unsplash Source
        cover_img = self.generate_goods_image(category.category_name)
        carousel_images = self.generate_carousel_images(cover_img)
        
        goods = Goods.objects.create(
            category=category,
            goods_name=goods_name,
            goods_price=base_price,
            market_price=market_price,
            cost_price=cost_price,
            goods_desc=goods_desc,
            goods_cover_img=cover_img,
            goods_carousel=carousel_images,
            goods_stock=random.randint(10, 1000),
            goods_sales=random.randint(0, 500),
            goods_status=random.choices([0, 1], weights=[1, 4])[0],  # 80%概率上架
            create_time=timezone.now() - timedelta(days=random.randint(0, 365))
        )
        
        return goods

    def generate_goods_name(self, category_name):
        """生成商品名称"""
        brands = ['苹果', '华为', '小米', '三星', '索尼', '戴尔', '联想', '耐克', '阿迪达斯', '优衣库']
        adjectives = ['新款', '旗舰', '豪华', '智能', '超薄', '高性能', '专业', '家用', '便携', '时尚']
        
        product_names = {
            '智能手机': ['手机', '智能手机', '5G手机'],
            '平板电脑': ['平板', '平板电脑', '学习平板'],
            '笔记本电脑': ['笔记本', '游戏本', '轻薄本'],
            '男装': ['T恤', '衬衫', '卫衣', '夹克'],
            '女装': ['连衣裙', '毛衣', '外套', '半身裙'],
            '食品': ['零食', '礼盒', '特产'],
            '家用电器': ['冰箱', '洗衣机', '空调', '电视'],
            '运动户外': ['跑鞋', '运动服', '帐篷', '自行车'],
            '美妆个护': ['面膜', '口红', '香水', '洗发水'],
            '图书文具': ['小说', '教材', '笔记本', '钢笔']
        }
        
        # 获取该类别的产品名称，如果没有则使用通用名称
        product_type = random.choice(product_names.get(category_name, ['商品']))
        
        return f"{random.choice(brands)} {random.choice(adjectives)}{product_type} {random.randint(1, 1000)}"

    def generate_goods_description(self, goods_name):
        """生成商品描述"""
        descriptions = [
            f"{goods_name}采用先进技术制造，具有出色的性能和耐用性。",
            f"这款{goods_name}设计精美，功能强大，是您日常使用的理想选择。",
            f"{goods_name}经过严格的质量检测，确保每一件产品都达到最高标准。"
        ]
        features = [
            "高性价比", "节能环保", "操作简便", "多功能一体", "智能控制",
            "防水防尘", "超长续航", "快速充电", "高清显示", "舒适手感"
        ]
        
        desc = random.choice(descriptions)
        desc += f" 产品特点：{', '.join(random.sample(features, min(3, len(features))))}。"
        desc += " 购买后享受7天无理由退货，1年质保服务。"
        
        return desc

    def generate_goods_image(self, category_name):
        """生成商品图片URL - 使用Unsplash Source"""
        category_keywords = {
            '智能手机': 'smartphone,phone,mobile',
            '平板电脑': 'tablet,ipad,device',
            '笔记本电脑': 'laptop,computer,notebook',
            '男装': 'mens clothing,fashion,apparel',
            '女装': 'womens clothing,dress,fashion',
            '食品': 'food,fruit,grocery',
            '家用电器': 'appliance,home,electronic',
            '运动户外': 'sports,outdoor,fitness',
            '美妆个护': 'cosmetic,beauty,makeup',
            '图书文具': 'book,stationery,office'
        }
        
        # 获取分类对应的关键词
        keywords = category_keywords.get(category_name, 'product')
        width, height = 800, 800
        
        return f'https://source.unsplash.com/{width}x{height}/?{keywords}'

    def generate_carousel_images(self, cover_img):
        """生成商品轮播图"""
        # 生成3-5张轮播图
        num_images = random.randint(3, 5)
        carousel_images = []
        
        for i in range(num_images):
            # 使用不同的Unsplash搜索词生成不同的图片
            search_terms = ['product', 'item', 'goods', 'merchandise', 'commodity']
            term = random.choice(search_terms)
            carousel_images.append(f'https://source.unsplash.com/800x800/?{term}&{i}')
        
        return carousel_images

    def create_goods_specs(self, goods):
        """创建商品规格 - 修复了random.sample错误"""
        spec_templates = {
            '电子产品': [
                ('颜色', ['黑色', '白色', '银色', '蓝色', '红色']),
                ('内存', ['8GB', '12GB', '16GB', '32GB']),
                ('存储', ['128GB', '256GB', '512GB', '1TB']),
                ('尺寸', ['小号', '中号', '大号'])
            ],
            '服装': [
                ('颜色', ['黑色', '白色', '灰色', '蓝色', '红色']),
                ('尺码', ['S', 'M', 'L', 'XL']),
                ('材质', ['棉', '涤纶', '尼龙', '羊毛'])
            ],
            '食品': [
                ('规格', ['500g', '1kg', '2kg']),
                ('口味', ['原味', '辣味', '甜味']),
                ('包装', ['袋装', '盒装', '罐装'])
            ],
            '默认': [
                ('颜色', ['黑色', '白色', '银色']),
                ('尺寸', ['标准', '大号']),
                ('型号', ['A型', 'B型'])
            ]
        }
        
        # 根据商品分类选择规格模板
        category_name = goods.category.category_name
        template_key = '默认'
        for key in spec_templates:
            if key in category_name:
                template_key = key
                break
        
        template = spec_templates[template_key]
        # 修复：确保抽取的数量不超过模板长度
        num_specs = min(random.randint(2, 4), len(template))
        specs = random.sample(template, num_specs)
        
        for spec_name, values in specs:
            spec_value = random.choice(values)
            GoodsSpec.objects.create(
                goods=goods,
                spec_name=spec_name,
                spec_value=spec_value
            )

    def create_goods_params(self, goods):
        """创建商品参数 - 修复了random.sample错误"""
        param_templates = {
            '电子产品': [
                ('品牌', lambda: random.choice(['苹果', '华为', '小米', '三星'])),
                ('型号', lambda: f"MODEL-{random.randint(1000, 9999)}"),
                ('处理器', lambda: random.choice(['Intel i5', 'Intel i7', 'AMD Ryzen 5'])),
                ('屏幕尺寸', lambda: f"{random.choice([13.3, 14, 15.6])}英寸")
            ],
            '服装': [
                ('品牌', lambda: random.choice(['耐克', '阿迪达斯', '优衣库', 'ZARA'])),
                ('材质', lambda: random.choice(['纯棉', '涤纶', '尼龙'])),
                ('产地', lambda: random.choice(['中国', '越南', '孟加拉']))
            ],
            '食品': [
                ('品牌', lambda: random.choice(['三只松鼠', '良品铺子', '百草味'])),
                ('生产日期', lambda: f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"),
                ('保质期', lambda: f"{random.randint(6, 24)}个月")
            ],
            '默认': [
                ('品牌', lambda: random.choice(['品牌A', '品牌B', '品牌C'])),
                ('型号', lambda: f"MODEL-{random.randint(100, 999)}"),
                ('产地', lambda: random.choice(['中国', '进口']))
            ]
        }
        
        # 根据商品分类选择参数模板
        category_name = goods.category.category_name
        template = param_templates.get('默认', [])
        for key in param_templates:
            if key in category_name:
                template = param_templates[key]
                break
        
        # 修复：确保抽取的数量不超过模板长度
        num_params = min(random.randint(3, 6), len(template))
        params = random.sample(template, num_params)
        
        for param_name, value_func in params:
            GoodsParam.objects.create(
                goods=goods,
                param_name=param_name,
                param_value=value_func()
            )