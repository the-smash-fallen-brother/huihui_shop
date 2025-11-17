import factory
from factory import fuzzy
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
import random
from .models import GoodsCategory, Goods, GoodsSpec, GoodsParam

# 电商品牌数据
ECOMMERCE_BRANDS = {
    '手机数码': ['Apple', '华为', '小米', 'OPPO', 'vivo', '三星', '荣耀', '一加', 'realme', '魅族'],
    '电脑办公': ['联想', '戴尔', '惠普', '华硕', '苹果', '华为', '微软', 'ThinkPad', 'MacBook', 'Surface'],
    '家用电器': ['海尔', '美的', '格力', '海信', 'TCL', '小米', '奥克斯', '格兰仕', '苏泊尔', '九阳'],
    '服装鞋帽': ['耐克', '阿迪达斯', '优衣库', 'ZARA', 'H&M', '李宁', '安踏', '特步', '361°', '匡威'],
    '美妆个护': ['兰蔻', '雅诗兰黛', '香奈儿', '迪奥', 'SK-II', '欧莱雅', '资生堂', '完美日记', '花西子', '珂润'],
    '食品生鲜': ['三只松鼠', '良品铺子', '百草味', '来伊份', '卫龙', '旺旺', '农夫山泉', '康师傅', '统一', '蒙牛'],
    '运动户外': ['耐克', '阿迪达斯', '安踏', '李宁', 'Under Armour', 'New Balance', '彪马', '斯凯奇', '回力', '飞跃'],
    '家居家装': ['宜家', '无印良品', '小米有品', '网易严选', '淘宝心选', '全友家居', '顾家家居', '曲美家居', '红木坊', '木匠世家'],
    '母婴玩具': ['帮宝适', '好奇', '花王', '美赞臣', '惠氏', '雅培', '乐高', '费雪', '芭比', '托马斯'],
    '图书文具': ['人民文学出版社', '商务印书馆', '中华书局', '中信出版社', '新东方', '晨光文具', '得力文具', '齐心文具', '三菱', '派克']
}

# 电商商品名称模板
ECOMMERCE_PRODUCTS = {
    '智能手机': [
        '{brand} {series} {model} {storage} {color}',
        '{brand} {series} {model} {storage} {color}',
        '{brand} {series} {model} {storage} {color}'
    ],
    '笔记本电脑': [
        '{brand} {series} {model} {cpu} {memory} {storage}',
        '{brand} {series} {model} {cpu} {memory} {storage}',
        '{brand} {series} {model} {cpu} {memory} {storage}'
    ],
    '空调': [
        '{brand} {series} {model} {power} {type}',
        '{brand} {series} {model} {power} {type}',
        '{brand} {series} {model} {power} {type}'
    ],
    '运动鞋': [
        '{brand} {series} {model} {color} {size}',
        '{brand} {series} {model} {color} {size}',
        '{brand} {series} {model} {color} {size}'
    ],
    '护肤品': [
        '{brand} {product} {size} {effect}',
        '{brand} {product} {size} {effect}',
        '{brand} {product} {size} {effect}'
    ]
}

class EcommerceCategoryFactory(factory.django.DjangoModelFactory):
    """电商分类工厂"""
    class Meta:
        model = GoodsCategory
    
    @classmethod
    def create_ecommerce_categories(cls):
        """创建电商分类体系"""
        categories_data = [
            {
                'name': '手机数码',
                'icon': '📱',
                'children': ['智能手机', '平板电脑', '智能手表', '蓝牙耳机', '充电器', '手机壳', '贴膜']
            },
            {
                'name': '电脑办公',
                'icon': '💻',
                'children': ['笔记本电脑', '台式机', '显示器', '键盘鼠标', '打印机', '办公软件', '路由器']
            },
            {
                'name': '家用电器',
                'icon': '🏠',
                'children': ['空调', '冰箱', '洗衣机', '电视', '热水器', '微波炉', '吸尘器', '电饭煲']
            },
            {
                'name': '服装鞋帽',
                'icon': '👕',
                'children': ['男装', '女装', '童装', '运动鞋', '休闲鞋', '帽子', '包包', '袜子']
            },
            {
                'name': '美妆个护',
                'icon': '💄',
                'children': ['面部护理', '彩妆', '香水', '洗护', '美发', '口腔护理', '身体护理']
            },
            {
                'name': '食品生鲜',
                'icon': '🍎',
                'children': ['零食饮料', '生鲜果蔬', '粮油调味', '茗茶', '酒类', '乳品', '保健品']
            },
            {
                'name': '运动户外',
                'icon': '⚽',
                'children': ['运动服装', '运动鞋', '健身器材', '球类运动', '户外装备', '水上运动', '骑行装备']
            },
            {
                'name': '家居家装',
                'icon': '🛋️',
                'children': ['家具', '家纺', '厨具', '收纳', '装饰', '灯具', '清洁工具', '床上用品']
            },
            {
                'name': '母婴玩具',
                'icon': '🧸',
                'children': ['奶粉辅食', '纸尿裤', '童装童鞋', '玩具', '喂养用品', '洗护用品', '孕产用品']
            },
            {
                'name': '图书文具',
                'icon': '📚',
                'children': ['图书', '教材教辅', '办公文具', '学生文具', '电子书', '期刊杂志', '音像制品']
            }
        ]
        
        created_categories = []
        for i, cat_data in enumerate(categories_data):
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
        
        return created_categories

class EcommerceGoodsFactory(factory.django.DjangoModelFactory):
    """电商商品工厂"""
    class Meta:
        model = Goods
    
    @classmethod
    def _generate_ecommerce_name(cls, category_name):
        """生成电商商品名称"""
        # 获取对应的品牌
        for key in ECOMMERCE_BRANDS:
            if key in category_name:
                brand = random.choice(ECOMMERCE_BRANDS[key])
                
                # 根据分类生成产品信息
                if '手机' in category_name:
                    series = random.choice(['Pro', 'Max', 'Plus', 'Ultra', 'Standard'])
                    model = random.randint(10, 20)
                    storage = random.choice(['128GB', '256GB', '512GB', '1TB'])
                    color = random.choice(['黑色', '白色', '银色', '蓝色', '红色', '绿色'])
                    return f"{brand} {series} {model} {storage} {color}"
                
                elif '电脑' in category_name or '笔记本' in category_name:
                    series = random.choice(['ThinkPad', 'EliteBook', 'MacBook', 'Latitude', 'Vostro'])
                    model = random.choice(['X1', 'X1 Carbon', 'E14', 'E15', 'Air', 'Pro'])
                    cpu = random.choice(['i5', 'i7', 'i9', 'M1', 'M2'])
                    memory = random.choice(['8GB', '16GB', '32GB'])
                    storage = random.choice(['256GB', '512GB', '1TB', '2TB'])
                    return f"{brand} {series} {model} {cpu}/{memory}/{storage}"
                
                elif '空调' in category_name:
                    series = random.choice(['智能', '变频', '静音', '节能'])
                    model = random.choice(['KFR-35GW', 'KFR-50LW', 'KFR-72LW'])
                    power = random.choice(['1.5匹', '2匹', '3匹'])
                    type_name = random.choice(['挂机', '柜机'])
                    return f"{brand} {series} {model} {power} {type_name}"
                
                elif '运动鞋' in category_name:
                    series = random.choice(['Air Max', 'Zoom', 'Ultra Boost', 'React', 'Flyknit'])
                    model = random.choice(['2023', '2024', 'Classic', 'Pro'])
                    color = random.choice(['黑/白', '红/白', '蓝/黑', '全黑', '全白'])
                    return f"{brand} {series} {model} {color}"
                
                elif '护肤' in category_name or '面部' in category_name:
                    product = random.choice(['精华液', '面霜', '眼霜', '爽肤水', '乳液'])
                    size = random.choice(['30ml', '50ml', '100ml', '150ml'])
                    effect = random.choice(['保湿', '美白', '抗衰老', '修复', '控油'])
                    return f"{brand} {product} {size} {effect}款"
                
                else:
                    # 通用产品名称
                    series = random.choice(['经典', '旗舰', '智能', '升级', '新款'])
                    model = random.randint(100, 999)
                    return f"{brand} {series} {model}"
        
        # 默认名称
        adjectives = ['新款', '升级款', '经典款', '智能', '高端', '实用']
        return f"通用品牌 {random.choice(adjectives)} {random.randint(100, 999)}"
    
    @classmethod
    def _generate_ecommerce_price(cls, category_name):
        """根据分类生成合理价格"""
        if '手机' in category_name:
            return random.uniform(1000, 8000)
        elif '电脑' in category_name or '笔记本' in category_name:
            return random.uniform(3000, 15000)
        elif '空调' in category_name or '冰箱' in category_name or '洗衣机' in category_name:
            return random.uniform(1500, 6000)
        elif '电视' in category_name:
            return random.uniform(2000, 10000)
        elif '运动鞋' in category_name:
            return random.uniform(200, 1500)
        elif '护肤' in category_name or '彩妆' in category_name:
            return random.uniform(50, 800)
        elif '食品' in category_name:
            return random.uniform(10, 200)
        elif '母婴' in category_name or '玩具' in category_name:
            return random.uniform(20, 500)
        elif '图书' in category_name:
            return random.uniform(10, 100)
        else:
            return random.uniform(100, 2000)
    
    goods_name = factory.LazyAttribute(lambda obj: obj._generate_ecommerce_name(obj.category.category_name))
    goods_price = factory.LazyAttribute(lambda obj: Decimal(str(obj._generate_ecommerce_price(obj.category.category_name))))
    
    goods_desc = factory.LazyAttribute(lambda obj: f"""
        【{obj.goods_name}】
        
        🌟 产品特点：
        ✅ 正品保证，官方授权
        ✅ 7天无理由退换
        ✅ 全国联保，售后无忧
        ✅ 极速发货，次日达
        
        📦 包装清单：
        • 主机 x1
        • 说明书 x1
        • 保修卡 x1
        • 配件套装
        
        💡 温馨提示：
        请在收货时当面验货，如有问题请及时联系客服。
        """)
    
    goods_cover_img = factory.LazyAttributeSequence(
        lambda obj, n: f'https://picsum.photos/seed/ecommerce{n}/800/800.jpg'
    )
    
    goods_carousel = factory.LazyAttributeSequence(
        lambda obj, n: [
            f'https://picsum.photos/seed/product{i}_{n}/800/800.jpg'
            for i in range(random.randint(3, 6))
        ]
    )
    
    goods_stock = fuzzy.FuzzyInteger(50, 2000)
    goods_sales = fuzzy.FuzzyInteger(0, 5000)
    goods_status = factory.LazyFunction(lambda: random.choices([0, 1], weights=[1, 9])[0])
    create_time = factory.LazyFunction(
        lambda: timezone.now() - timedelta(days=random.randint(1, 180))
    )
    
    @factory.lazy_attribute
    def market_price(self):
        return self.goods_price * Decimal('1.3')
    
    @factory.lazy_attribute
    def cost_price(self):
        return self.goods_price * Decimal('0.6')
    
    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        """确保有分类"""
        if 'category' not in kwargs:
            # 获取一个二级分类
            level2_categories = GoodsCategory.objects.filter(category_level=2)
            if level2_categories.exists():
                kwargs['category'] = random.choice(level2_categories)
        
        return kwargs

class EcommerceSpecFactory(factory.django.DjangoModelFactory):
    """电商规格工厂"""
    class Meta:
        model = GoodsSpec
    
    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        """根据分类生成规格"""
        goods = kwargs.get('goods')
        if goods:
            category_name = goods.category.category_name
            
            # 根据分类生成规格
            spec_templates = {
                '手机': [
                    ('颜色', ['深空灰', '银色', '金色', '玫瑰金', '蓝色', '红色', '绿色']),
                    ('内存', ['4GB+64GB', '6GB+128GB', '8GB+256GB', '12GB+512GB', '12GB+1TB']),
                    ('网络', ['4G全网通', '5G全网通']),
                    ('版本', ['国行', '港版', '美版', '日版'])
                ],
                '笔记本': [
                    ('处理器', ['Intel i5', 'Intel i7', 'Intel i9', 'AMD R5', 'AMD R7', 'M1', 'M2']),
                    ('内存', ['8GB', '16GB', '32GB', '64GB']),
                    ('硬盘', ['256GB SSD', '512GB SSD', '1TB SSD', '2TB SSD']),
                    ('显卡', ['集成显卡', 'MX350', 'RTX3050', 'RTX3060', 'RTX3070']),
                    ('屏幕尺寸', ['13.3英寸', '14英寸', '15.6英寸', '16英寸', '17.3英寸'])
                ],
                '空调': [
                    ('匹数', ['1匹', '1.5匹', '2匹', '2.5匹', '3匹', '5匹']),
                    ('类型', ['挂机', '柜机', '中央空调']),
                    ('能效等级', ['一级能效', '二级能效', '三级能效']),
                    ('功能', ['单冷', '冷暖', '变频', '智能控制'])
                ],
                '运动鞋': [
                    ('尺码', ['36', '37', '38', '39', '40', '41', '42', '43', '44', '45']),
                    ('颜色', ['黑色', '白色', '红色', '蓝色', '灰色', '彩色']),
                    ('鞋码类型', ['标准码', '偏大半码', '偏小半码']),
                    ('适用场景', ['跑步', '篮球', '休闲', '训练'])
                ],
                '护肤': [
                    ('规格', ['30ml', '50ml', '100ml', '150ml', '200ml']),
                    ('功效', ['保湿', '美白', '抗衰老', '修复', '控油', '祛痘']),
                    ('适用肤质', ['干性', '油性', '混合性', '敏感性']),
                    ('产地', ['中国', '日本', '韩国', '美国', '法国'])
                ]
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
                kwargs['spec_name'] = random.choice(['颜色', '尺寸', '规格', '型号'])
                kwargs['spec_value'] = random.choice(['标准款', '升级款', '豪华版'])
        
        return kwargs

class EcommerceParamFactory(factory.django.DjangoModelFactory):
    """电商参数工厂"""
    class Meta:
        model = GoodsParam
    
    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        """根据分类生成参数"""
        goods = kwargs.get('goods')
        if goods:
            category_name = goods.category.category_name
            
            # 根据分类生成参数
            param_templates = {
                '手机': [
                    ('品牌', lambda: random.choice(ECOMMERCE_BRANDS['手机数码'])),
                    ('型号', lambda: f"MO-{random.randint(1000, 9999)}"),
                    ('屏幕尺寸', lambda: f"{random.choice([5.8, 6.1, 6.5, 6.7])}英寸"),
                    ('电池容量', lambda: f"{random.choice([4000, 4500, 5000, 5500])}mAh"),
                    ('摄像头', lambda: f"{random.choice([4800, 5000, 6400])}万像素"),
                    ('操作系统', lambda: random.choice(['Android 12', 'Android 13', 'iOS 15', 'iOS 16'])),
                    ('上市时间', lambda: f"{random.randint(2022, 2024)}年{random.randint(1, 12)}月")
                ],
                '笔记本': [
                    ('品牌', lambda: random.choice(ECOMMERCE_BRANDS['电脑办公'])),
                    ('CPU型号', lambda: random.choice(['i5-1135G7', 'i7-1165G7', 'R5-5500U', 'R7-5800H', 'M1', 'M2'])),
                    ('内存类型', lambda: random.choice(['DDR4', 'LPDDR4', 'LPDDR5'])),
                    ('硬盘类型', lambda: random.choice(['SSD', 'NVMe SSD'])),
                    ('屏幕分辨率', lambda: random.choice(['1920x1080', '2560x1440', '2880x1800', '3840x2160'])),
                    ('重量', lambda: f"{random.uniform(1.0, 3.0):.1f}kg"),
                    ('保修期', lambda: f"{random.randint(1, 3)}年")
                ],
                '空调': [
                    ('品牌', lambda: random.choice(ECOMMERCE_BRANDS['家用电器'])),
                    ('制冷量', lambda: f"{random.randint(3200, 7200)}W"),
                    ('制热量', lambda: f"{random.randint(3500, 8000)}W"),
                    ('噪音值', lambda: f"{random.randint(20, 45)}dB"),
                    ('适用面积', lambda: f"{random.randint(10, 50)}㎡"),
                    ('电源', lambda: "220V/50Hz"),
                    ('保修期', lambda: f"{random.randint(3, 6)}年")
                ],
                '运动鞋': [
                    ('品牌', lambda: random.choice(ECOMMERCE_BRANDS['服装鞋帽'])),
                    ('材质', lambda: random.choice(['真皮', '合成革', '网面', '帆布'])),
                    ('鞋底材质', lambda: random.choice(['橡胶底', 'EVA底', 'PU底'])),
                    ('产地', lambda: random.choice(['中国', '越南', '印度尼西亚', '泰国'])),
                    ('上市时间', lambda: f"{random.randint(2022, 2024)}年春夏/秋冬")
                ],
                '护肤': [
                    ('品牌', lambda: random.choice(ECOMMERCE_BRANDS['美妆个护'])),
                    ('保质期', lambda: f"{random.randint(2, 5)}年"),
                    ('产地', lambda: random.choice(['中国', '日本', '韩国', '法国', '美国'])),
                    ('适用年龄', lambda: random.choice(['18-25岁', '25-35岁', '35-45岁', '45岁以上'])),
                    ('是否进口', lambda: random.choice(['是', '否']))
                ]
            }
            
            # 匹配分类
            for key in param_templates:
                if key in category_name:
                    param_data = random.choice(param_templates[key])
                    kwargs['param_name'] = param_data[0]
                    kwargs['param_value'] = param_data[1]()
                    break
            else:
                # 默认参数
                kwargs['param_name'] = random.choice(['品牌', '产地', '保修期', '材质'])
                kwargs['param_value'] = random.choice(['中国品牌', '进口商品', '1年保修', '优质材料'])
        
        return kwargs