import factory
from factory import fuzzy
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
import random
from .models import GoodsCategory, Goods, GoodsSpec, GoodsParam

# 电商品牌数据
ECOMMERCE_BRANDS = {
    '手机数码': ['Apple', '华为', '小米', 'OPPO', 'vivo', '三星', '荣耀', '一加', '魅族', 'realme'],
    '电脑办公': ['联想', '戴尔', '惠普', '华硕', '苹果', '华为', '微软', '神舟', '宏碁', '微星'],
    '家用电器': ['海尔', '美的', '格力', '海信', 'TCL', '小米', '奥克斯', '志高', '长虹', '康佳'],
    '服装鞋帽': ['耐克', '阿迪达斯', '优衣库', 'ZARA', 'H&M', '李宁', '安踏', '特步', '361°', '鸿星尔克'],
    '美妆个护': ['兰蔻', '雅诗兰黛', '香奈儿', '迪奥', 'SK-II', '欧莱雅', '资生堂', '完美日记', '花西子', '薇诺娜'],
    '食品生鲜': ['三只松鼠', '良品铺子', '百草味', '来伊份', '卫龙', '旺旺', '盼盼', '恰恰', '康师傅', '统一'],
    '运动户外': ['耐克', '阿迪达斯', '安踏', '李宁', 'Under Armour', 'New Balance', '迪卡侬', '北面', '始祖鸟', '哥伦比亚'],
    '家居家装': ['宜家', '无印良品', '小米有品', '网易严选', '淘宝心选', '顾家家居', '全友家居', '曲美家居', '红星美凯龙', '居然之家'],
    '母婴玩具': ['帮宝适', '好奇', '花王', '美赞臣', '惠氏', '雅培', '乐高', '费雪', '贝亲', '好孩子'],
    '图书文具': ['人民文学出版社', '商务印书馆', '中华书局', '中信出版社', '新东方', '晨光文具', '得力文具', '齐心文具', '广博文具', '真彩文具']
}

# 真实商品图片URL映射表 - 使用DummyJSON.com的真实商品图片
ECOMMERCE_IMAGES = {
    '智能手机': [
        'https://i.dummyjson.com/data/products/1/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/2/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/3/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/4/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/5/thumbnail.jpg'
    ],
    '平板电脑': [
        'https://i.dummyjson.com/data/products/6/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/7/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/8/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/9/thumbnail.jpg'
    ],
    '智能手表': [
        'https://i.dummyjson.com/data/products/10/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/11/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/12/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/13/thumbnail.jpg'
    ],
    '蓝牙耳机': [
        'https://i.dummyjson.com/data/products/14/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/15/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/16/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/17/thumbnail.jpg'
    ],
    '手机壳': [
        'https://i.dummyjson.com/data/products/18/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/19/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/20/thumbnail.jpg'
    ],
    '贴膜': [
        'https://i.dummyjson.com/data/products/21/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/22/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/23/thumbnail.jpg'
    ],
    '笔记本电脑': [
        'https://i.dummyjson.com/data/products/24/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/25/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/26/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/27/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/28/thumbnail.jpg'
    ],
    '台式机': [
        'https://i.dummyjson.com/data/products/29/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/30/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/31/thumbnail.jpg'
    ],
    '显示器': [
        'https://i.dummyjson.com/data/products/32/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/33/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/34/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/35/thumbnail.jpg'
    ],
    '键盘鼠标': [
        'https://i.dummyjson.com/data/products/36/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/37/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/38/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/39/thumbnail.jpg'
    ],
    '打印机': [
        'https://i.dummyjson.com/data/products/40/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/41/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/42/thumbnail.jpg'
    ],
    '办公软件': [
        'https://i.dummyjson.com/data/products/43/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/44/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/45/thumbnail.jpg'
    ],
    '路由器': [
        'https://i.dummyjson.com/data/products/46/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/47/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/48/thumbnail.jpg'
    ],
    '空调': [
        'https://i.dummyjson.com/data/products/49/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/50/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/51/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/52/thumbnail.jpg'
    ],
    '冰箱': [
        'https://i.dummyjson.com/data/products/53/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/54/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/55/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/56/thumbnail.jpg'
    ],
    '洗衣机': [
        'https://i.dummyjson.com/data/products/57/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/58/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/59/thumbnail.jpg'
    ],
    '电视': [
        'https://i.dummyjson.com/data/products/60/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/61/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/62/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/63/thumbnail.jpg'
    ],
    '热水器': [
        'https://i.dummyjson.com/data/products/64/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/65/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/66/thumbnail.jpg'
    ],
    '微波炉': [
        'https://i.dummyjson.com/data/products/67/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/68/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/69/thumbnail.jpg'
    ],
    '吸尘器': [
        'https://i.dummyjson.com/data/products/70/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/71/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/72/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/73/thumbnail.jpg'
    ],
    '男装': [
        'https://i.dummyjson.com/data/products/74/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/75/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/76/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/77/thumbnail.jpg'
    ],
    '女装': [
        'https://i.dummyjson.com/data/products/78/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/79/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/80/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/81/thumbnail.jpg'
    ],
    '童装': [
        'https://i.dummyjson.com/data/products/82/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/83/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/84/thumbnail.jpg'
    ],
    '运动鞋': [
        'https://i.dummyjson.com/data/products/85/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/86/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/87/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/88/thumbnail.jpg'
    ],
    '休闲鞋': [
        'https://i.dummyjson.com/data/products/89/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/90/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/91/thumbnail.jpg'
    ],
    '帽子': [
        'https://i.dummyjson.com/data/products/92/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/93/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/94/thumbnail.jpg'
    ],
    '包包': [
        'https://i.dummyjson.com/data/products/95/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/96/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/97/thumbnail.jpg'
    ],
    '面部护理': [
        'https://i.dummyjson.com/data/products/98/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/99/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/100/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/101/thumbnail.jpg'
    ],
    '彩妆': [
        'https://i.dummyjson.com/data/products/102/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/103/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/104/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/105/thumbnail.jpg'
    ],
    '香水': [
        'https://i.dummyjson.com/data/products/106/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/107/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/108/thumbnail.jpg'
    ],
    '洗护': [
        'https://i.dummyjson.com/data/products/109/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/110/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/111/thumbnail.jpg'
    ],
    '美发': [
        'https://i.dummyjson.com/data/products/112/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/113/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/114/thumbnail.jpg'
    ],
    '口腔护理': [
        'https://i.dummyjson.com/data/products/115/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/116/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/117/thumbnail.jpg'
    ],
    '身体护理': [
        'https://i.dummyjson.com/data/products/118/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/119/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/120/thumbnail.jpg'
    ],
    '零食饮料': [
        'https://i.dummyjson.com/data/products/121/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/122/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/123/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/124/thumbnail.jpg'
    ],
    '生鲜果蔬': [
        'https://i.dummyjson.com/data/products/125/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/126/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/127/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/128/thumbnail.jpg'
    ],
    '粮油调味': [
        'https://i.dummyjson.com/data/products/129/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/130/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/131/thumbnail.jpg'
    ],
    '茗茶': [
        'https://i.dummyjson.com/data/products/132/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/133/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/134/thumbnail.jpg'
    ],
    '酒类': [
        'https://i.dummyjson.com/data/products/135/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/136/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/137/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/138/thumbnail.jpg'
    ],
    '运动服装': [
        'https://i.dummyjson.com/data/products/139/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/140/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/141/thumbnail.jpg'
    ],
    '健身器材': [
        'https://i.dummyjson.com/data/products/142/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/143/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/144/thumbnail.jpg'
    ],
    '球类运动': [
        'https://i.dummyjson.com/data/products/145/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/146/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/147/thumbnail.jpg'
    ],
    '户外装备': [
        'https://i.dummyjson.com/data/products/148/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/149/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/150/thumbnail.jpg'
    ],
    '水上运动': [
        'https://i.dummyjson.com/data/products/151/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/152/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/153/thumbnail.jpg'
    ],
    '骑行装备': [
        'https://i.dummyjson.com/data/products/154/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/155/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/156/thumbnail.jpg'
    ],
    '家具': [
        'https://i.dummyjson.com/data/products/157/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/158/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/159/thumbnail.jpg'
    ],
    '家纺': [
        'https://i.dummyjson.com/data/products/160/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/161/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/162/thumbnail.jpg'
    ],
    '厨具': [
        'https://i.dummyjson.com/data/products/163/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/164/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/165/thumbnail.jpg'
    ],
    '收纳': [
        'https://i.dummyjson.com/data/products/166/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/167/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/168/thumbnail.jpg'
    ],
    '装饰': [
        'https://i.dummyjson.com/data/products/169/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/170/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/171/thumbnail.jpg'
    ],
    '灯具': [
        'https://i.dummyjson.com/data/products/172/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/173/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/174/thumbnail.jpg'
    ],
    '清洁工具': [
        'https://i.dummyjson.com/data/products/175/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/176/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/177/thumbnail.jpg'
    ],
    '床上用品': [
        'https://i.dummyjson.com/data/products/178/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/179/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/180/thumbnail.jpg'
    ],
    '奶粉辅食': [
        'https://i.dummyjson.com/data/products/181/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/182/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/183/thumbnail.jpg'
    ],
    '纸尿裤': [
        'https://i.dummyjson.com/data/products/184/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/185/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/186/thumbnail.jpg'
    ],
    '童装童鞋': [
        'https://i.dummyjson.com/data/products/187/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/188/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/189/thumbnail.jpg'
    ],
    '玩具': [
        'https://i.dummyjson.com/data/products/190/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/191/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/192/thumbnail.jpg'
    ],
    '喂养用品': [
        'https://i.dummyjson.com/data/products/193/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/194/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/195/thumbnail.jpg'
    ],
    '洗护用品': [
        'https://i.dummyjson.com/data/products/196/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/197/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/198/thumbnail.jpg'
    ],
    '孕产用品': [
        'https://i.dummyjson.com/data/products/199/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/200/thumbnail.jpg'
    ],
    '图书': [
        'https://i.dummyjson.com/data/products/201/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/202/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/203/thumbnail.jpg'
    ],
    '教材教辅': [
        'https://i.dummyjson.com/data/products/204/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/205/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/206/thumbnail.jpg'
    ],
    '办公文具': [
        'https://i.dummyjson.com/data/products/207/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/208/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/209/thumbnail.jpg'
    ],
    '学生文具': [
        'https://i.dummyjson.com/data/products/210/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/211/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/212/thumbnail.jpg'
    ],
    '电子书': [
        'https://i.dummyjson.com/data/products/213/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/214/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/215/thumbnail.jpg'
    ],
    '期刊杂志': [
        'https://i.dummyjson.com/data/products/216/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/217/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/218/thumbnail.jpg'
    ],
    '音像制品': [
        'https://i.dummyjson.com/data/products/219/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/220/thumbnail.jpg',
        'https://i.dummyjson.com/data/products/221/thumbnail.jpg'
    ]
}

def generate_ecommerce_name(category_name):
    """生成电商商品名称"""
    # 分类名称到品牌类别的映射
    category_to_brand_key = {
        '智能手机': '手机数码', '平板电脑': '手机数码', '智能手表': '手机数码', 
        '蓝牙耳机': '手机数码', '手机壳': '手机数码', '贴膜': '手机数码',
        '笔记本电脑': '电脑办公', '台式机': '电脑办公', '显示器': '电脑办公', 
        '键盘鼠标': '电脑办公', '打印机': '电脑办公', '办公软件': '电脑办公', '路由器': '电脑办公',
        '空调': '家用电器', '冰箱': '家用电器', '洗衣机': '家用电器', '电视': '家用电器', 
        '热水器': '家用电器', '微波炉': '家用电器', '吸尘器': '家用电器', '电饭煲': '家用电器',
        '男装': '服装鞋帽', '女装': '服装鞋帽', '童装': '服装鞋帽', '运动鞋': '服装鞋帽', 
        '休闲鞋': '服装鞋帽', '帽子': '服装鞋帽', '包包': '服装鞋帽', '袜子': '服装鞋帽',
        '面部护理': '美妆个护', '彩妆': '美妆个护', '香水': '美妆个护', '洗护': '美妆个护', 
        '美发': '美妆个护', '口腔护理': '美妆个护', '身体护理': '美妆个护',
        '零食饮料': '食品生鲜', '生鲜果蔬': '食品生鲜', '粮油调味': '食品生鲜', 
        '茗茶': '食品生鲜', '酒类': '食品生鲜', '乳品': '食品生鲜', '保健品': '食品生鲜',
        '运动服装': '运动户外', '健身器材': '运动户外', '球类运动': '运动户外', 
        '户外装备': '运动户外', '水上运动': '运动户外', '骑行装备': '运动户外',
        '家具': '家居家装', '家纺': '家居家装', '厨具': '家居家装', '收纳': '家居家装', 
        '装饰': '家居家装', '灯具': '家居家装', '清洁工具': '家居家装', '床上用品': '家居家装',
        '奶粉辅食': '母婴玩具', '纸尿裤': '母婴玩具', '童装童鞋': '母婴玩具', 
        '玩具': '母婴玩具', '喂养用品': '母婴玩具', '洗护用品': '母婴玩具', '孕产用品': '母婴玩具',
        '图书': '图书文具', '教材教辅': '图书文具', '办公文具': '图书文具', '学生文具': '图书文具', 
        '电子书': '图书文具', '期刊杂志': '图书文具', '音像制品': '图书文具'
    }
    
    # 获取对应的品牌类别
    brand_key = category_to_brand_key.get(category_name)
    if brand_key and brand_key in ECOMMERCE_BRANDS:
        brand = random.choice(ECOMMERCE_BRANDS[brand_key])
    else:
        # 回退到包含匹配
        brand = None
        for key in ECOMMERCE_BRANDS:
            if key in category_name or category_name in key:
                brand = random.choice(ECOMMERCE_BRANDS[key])
                break
        if not brand:
            brand = random.choice(['Apple', '华为', '小米', '耐克', '美的'])  # 默认品牌
    
    # 根据具体分类生成商品名称
    if category_name == '智能手机':
        models = [
            f"{brand} iPhone 15 Pro Max 256GB 原色钛金属",
            f"{brand} iPhone 15 Pro 256GB 蓝色钛金属",
            f"{brand} iPhone 15 Plus 256GB 粉色",
            f"{brand} iPhone 15 128GB 黑色",
            f"{brand} Mate 60 Pro 512GB 雅川青",
            f"{brand} Mate 60 Pro+ 512GB 宣白",
            f"{brand} Mate 60 256GB 雅黑",
            f"{brand} 小米14 Pro 12GB+256GB 黑色",
            f"{brand} 小米14 12GB+256GB 白色",
            f"{brand} Find X6 Pro 16GB+256GB 飞泉绿",
            f"{brand} Find X6 12GB+256GB 飞泉绿",
            f"{brand} X100 Pro 12GB+256GB 星迹蓝",
            f"{brand} X100 12GB+256GB 星迹蓝"
        ]
        return random.choice(models)
    
    elif category_name == '笔记本电脑':
        models = [
            f"{brand} MacBook Pro 14英寸 M3 Pro芯片 18GB内存 512GB SSD 深空黑色",
            f"{brand} MacBook Air 13英寸 M3芯片 8GB内存 256GB SSD 午夜色",
            f"{brand} ThinkPad X1 Carbon Gen 11 14英寸 i7-1365U 16GB 1TB SSD",
            f"{brand} ThinkPad T14 Gen 4 14英寸 i5-1335U 16GB 512GB SSD",
            f"{brand} XPS 13 Plus 13.4英寸 i7-1360P 16GB 512GB SSD",
            f"{brand} XPS 15 15.6英寸 i7-13700H 32GB 1TB SSD RTX4060",
            f"{brand} HP Spectre x360 14英寸 i7-1355U 16GB 1TB SSD",
            f"{brand} HP EliteBook 840 G10 14英寸 i5-1335U 16GB 512GB SSD"
        ]
        return random.choice(models)
    
    elif category_name == '空调':
        models = [
            f"{brand} 变频冷暖空调 1.5匹 一级能效 KFR-35GW/NhGe1B",
            f"{brand} 智能空调 1.5匹 新一级能效 KFR-35GW/N8VHA1",
            f"{brand} 变频空调 2匹 一级能效 柜机 KFR-50LW/N8KHA1",
            f"{brand} 新一级能效空调 1.5匹 挂机 KFR-35GW/NhV1B1",
            f"{brand} 智能变频空调 1.5匹 一级能效 KFR-35GW/BDN8-X1"
        ]
        return random.choice(models)
    
    elif category_name == '运动鞋':
        models = [
            f"{brand} Air Max 270 React 运动鞋 白色/黑色 CI3899-100",
            f"{brand} Air Force 1 Low 经典百搭小白鞋 CT0997-100",
            f"{brand} Ultra Boost 22 跑步鞋 黑色/碳灰 S22995",
            f"{brand} Stan Smith 经典绿尾小白鞋 C77124",
            f"{brand} 迪桑特 Descente 缓震跑步鞋 EKOPRU15090",
            f"{brand} 越野徒步鞋 A-FLASHFOAM 4.0 运动鞋",
            f"{brand} 安踏 马赫4代 跑步鞋 2023新款",
            f"{brand} 李宁 超轻20代 跑鞋 轻量透气"
        ]
        return random.choice(models)
    
    elif category_name in ['面部护理', '彩妆']:
        models = [
            f"{brand} 小黑瓶精华肌底液 50ml 抗老修护",
            f"{brand} 兰蔻菁纯面霜 60ml 紧致淡纹",
            f"{brand} 小棕瓶修护精华 50ml 抗蓝光",
            f"{brand} 雅诗兰黛智妍面霜 50ml 滋润修护",
            f"{brand} SK-II神仙水护肤精华露 230ml 补水保湿",
            f"{brand} 香奈儿山茶花保湿精华露 30ml",
            f"{brand} 迪奥烈艳蓝金唇膏 999# 正红色",
            f"{brand} 阿玛尼红管唇釉 405# 烂番茄色"
        ]
        return random.choice(models)
    
    elif category_name == '电视':
        models = [
            f"{brand} 55英寸 4K超高清 QLED量子点游戏电视 QA55Q60CAJXXZ",
            f"{brand} 65英寸 OLED自发光屏 游戏电视 KD-65A80EK",
            f"{brand} 75英寸 Mini LED 4K超高清 Q10G Pro",
            f"{brand} 65英寸 ULED Mini LED 65E8H",
            f"{brand} 75英寸 OLED电视 77C2"
        ]
        return random.choice(models)
    
    elif category_name == '冰箱':
        models = [
            f"{brand} 501升 十字对开门双开门 BCD-501WGHFD14S8U1",
            f"{brand} 521升 十字对开四门冰箱 BCD-521WSSKMD",
            f"{brand} 550升 变频风冷无霜 十字对开门 BCD-550WKFDT1S",
            f"{brand} 600升 十字对开四门冰箱 RS62N8004SL",
            f"{brand} 635升 对开门冰箱 KFR600LW"
        ]
        return random.choice(models)
    
    else:
        series = random.choice(['经典', '旗舰', '智能', '升级', 'Pro', 'Max'])
        model = random.randint(100, 999)
        return f"{brand} {series}款 {model}"

def get_ecommerce_image(category_name):
    """获取简单的商品图片URL - 快速加载，纯英文URL"""
    # 分类名称到英文映射
    category_to_english = {
        '智能手机': 'smartphone', '平板电脑': 'tablet', '智能手表': 'smartwatch', 
        '蓝牙耳机': 'headphones', '充电器': 'charger', '手机壳': 'phonecase', '贴膜': 'screenprotector',
        '笔记本电脑': 'laptop', '台式机': 'desktop', '显示器': 'monitor', 
        '键盘鼠标': 'keyboard', '打印机': 'printer', '办公软件': 'software', '路由器': 'router',
        '空调': 'airconditioner', '冰箱': 'refrigerator', '洗衣机': 'washingmachine', '电视': 'tv', 
        '热水器': 'heater', '微波炉': 'microwave', '吸尘器': 'vacuum', '电饭煲': 'cooker',
        '男装': 'menswear', '女装': 'womenswear', '童装': 'kidswear', '运动鞋': 'shoes', 
        '休闲鞋': 'casualshoes', '帽子': 'hat', '包包': 'bag', '袜子': 'socks',
        '面部护理': 'skincare', '彩妆': 'makeup', '香水': 'perfume', '洗护': 'bodycare', 
        '美发': 'haircare', '口腔护理': 'oralcare', '身体护理': 'bodylotion',
        '零食饮料': 'snacks', '生鲜果蔬': 'freshfood', '粮油调味': 'groceries', 
        '茗茶': 'tea', '酒类': 'wine', '乳品': 'milk', '保健品': 'supplements',
        '运动服装': 'sportswear', '健身器材': 'fitness', '球类运动': 'sports', 
        '户外装备': 'outdoor', '水上运动': 'watersports', '骑行装备': 'cycling',
        '家具': 'furniture', '家纺': 'hometextile', '厨具': 'kitchen', '收纳': 'storage', 
        '装饰': 'decor', '灯具': 'lighting', '清洁工具': 'cleaning', '床上用品': 'bedding',
        '奶粉辅食': 'babyfood', '纸尿裤': 'diapers', '童装童鞋': 'kidsshoe', 
        '玩具': 'toys', '喂养用品': 'feeding', '洗护用品': 'babycare', '孕产用品': 'maternity',
        '图书': 'books', '教材教辅': 'textbooks', '办公文具': 'stationery', '学生文具': 'school', 
        '电子书': 'ebook', '期刊杂志': 'magazines', '音像制品': 'media'
    }
    
    # 获取对应的英文标识
    english_name = category_to_english.get(category_name, 'product')
    
    # 生成简单纯英文的图片URL
    image_id = random.randint(1, 999)
    return f"https://picsum.photos/seed/{english_name}-{image_id}/800/800.jpg"

def get_ecommerce_image(category_name):
    """获取简单的商品图片URL - 快速加载，纯英文URL"""
    # 分类名称到英文映射
    category_to_english = {
        '智能手机': 'smartphone', '平板电脑': 'tablet', '智能手表': 'smartwatch', 
        '蓝牙耳机': 'headphones', '充电器': 'charger', '手机壳': 'phonecase', '贴膜': 'screenprotector',
        '笔记本电脑': 'laptop', '台式机': 'desktop', '显示器': 'monitor', 
        '键盘鼠标': 'keyboard', '打印机': 'printer', '办公软件': 'software', '路由器': 'router',
        '空调': 'airconditioner', '冰箱': 'refrigerator', '洗衣机': 'washingmachine', '电视': 'tv', 
        '热水器': 'heater', '微波炉': 'microwave', '吸尘器': 'vacuum', '电饭煲': 'cooker',
        '男装': 'menswear', '女装': 'womenswear', '童装': 'kidswear', '运动鞋': 'shoes', 
        '休闲鞋': 'casualshoes', '帽子': 'hat', '包包': 'bag', '袜子': 'socks',
        '面部护理': 'skincare', '彩妆': 'makeup', '香水': 'perfume', '洗护': 'bodycare', 
        '美发': 'haircare', '口腔护理': 'oralcare', '身体护理': 'bodylotion',
        '零食饮料': 'snacks', '生鲜果蔬': 'freshfood', '粮油调味': 'groceries', 
        '茗茶': 'tea', '酒类': 'wine', '乳品': 'milk', '保健品': 'supplements',
        '运动服装': 'sportswear', '健身器材': 'fitness', '球类运动': 'sports', 
        '户外装备': 'outdoor', '水上运动': 'watersports', '骑行装备': 'cycling',
        '家具': 'furniture', '家纺': 'hometextile', '厨具': 'kitchen', '收纳': 'storage', 
        '装饰': 'decor', '灯具': 'lighting', '清洁工具': 'cleaning', '床上用品': 'bedding',
        '奶粉辅食': 'babyfood', '纸尿裤': 'diapers', '童装童鞋': 'kidsshoe', 
        '玩具': 'toys', '喂养用品': 'feeding', '洗护用品': 'babycare', '孕产用品': 'maternity',
        '图书': 'books', '教材教辅': 'textbooks', '办公文具': 'stationery', '学生文具': 'school', 
        '电子书': 'ebook', '期刊杂志': 'magazines', '音像制品': 'media'
    }
    
    # 获取对应的英文标识
    english_name = category_to_english.get(category_name, 'product')
    
    # 生成简单纯英文的图片URL
    image_id = random.randint(1, 999)
    return f"https://picsum.photos/seed/{english_name}-{image_id}/800/800.jpg"

def generate_ecommerce_price(category_name):
    """根据分类生成合理价格"""
    if '手机' in category_name:
        return random.uniform(1000, 8000)
    elif '电脑' in category_name or '笔记本' in category_name:
        return random.uniform(3000, 15000)
    elif '空调' in category_name or '冰箱' in category_name:
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
class SimpleEcommerceGoodsFactory(factory.django.DjangoModelFactory):
    """简化版电商商品工厂"""
    class Meta:
        model = Goods
    
    # 先设置默认值，然后在调整时重新生成
    goods_name = factory.Faker('word')
    goods_price = fuzzy.FuzzyDecimal(100, 2000, 2)
    
    goods_desc = factory.Faker('paragraph')
    
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
    
    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        """确保有分类并生成电商数据"""
        if 'category' not in kwargs:
            # 获取一个二级分类
            level2_categories = GoodsCategory.objects.filter(category_level=2)
            if level2_categories.exists():
                kwargs['category'] = random.choice(level2_categories)
        
        # 生成真实的电商名称和价格
        category_name = kwargs['category'].category_name
        kwargs['goods_name'] = generate_ecommerce_name(category_name)
        kwargs['goods_price'] = Decimal(str(generate_ecommerce_price(category_name)))
        
        # 生成真实的商品图片
        kwargs['goods_cover_img'] = get_ecommerce_image(category_name)
        
        # 生成轮播图
        base_seed = category_name.replace(' ', '').lower()
        kwargs['goods_carousel'] = [
            f"https://picsum.photos/seed/{base_seed}_{i}/800/800.jpg" 
            for i in range(random.randint(3, 6))
        ]
        
        # 生成商品描述
        kwargs['goods_desc'] = f"""
【{kwargs['goods_name']}】

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
        """
        
        return kwargs
    
    @factory.lazy_attribute
    def market_price(self):
        return self.goods_price * Decimal('1.3')
    
    @factory.lazy_attribute
    def cost_price(self):
        return self.goods_price * Decimal('0.6')

def create_ecommerce_categories():
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
    
    # 清除现有分类
    GoodsCategory.objects.all().delete()
    
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

def create_ecommerce_specs(goods):
    """创建电商商品规格"""
    category_name = goods.category.category_name
    
    spec_templates = {
        '手机': [
            ('颜色', ['深空灰', '银色', '金色', '玫瑰金', '蓝色', '红色']),
            ('内存', ['4GB+64GB', '6GB+128GB', '8GB+256GB', '12GB+512GB']),
            ('网络', ['4G全网通', '5G全网通']),
            ('版本', ['国行', '港版', '美版', '日版'])
        ],
        '笔记本': [
            ('处理器', ['Intel i5', 'Intel i7', 'AMD R5', 'AMD R7', 'M1', 'M2']),
            ('内存', ['8GB', '16GB', '32GB']),
            ('硬盘', ['256GB SSD', '512GB SSD', '1TB SSD']),
            ('显卡', ['集成显卡', 'MX350', 'RTX3050', 'RTX3060']),
            ('屏幕尺寸', ['13.3英寸', '14英寸', '15.6英寸', '16英寸'])
        ],
        '空调': [
            ('匹数', ['1匹', '1.5匹', '2匹', '2.5匹', '3匹', '5匹']),
            ('类型', ['挂机', '柜机', '中央空调']),
            ('能效等级', ['一级能效', '二级能效', '三级能效']),
            ('功能', ['单冷', '冷暖', '变频', '智能控制'])
        ],
        '运动鞋': [
            ('尺码', ['36', '37', '38', '39', '40', '41', '42', '43', '44', '45']),
            ('颜色', ['黑色', '白色', '红色', '蓝色', '灰色']),
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
            num_specs = random.randint(2, 4)
            selected_specs = random.sample(spec_templates[key], min(num_specs, len(spec_templates[key])))
            
            for spec_name, spec_values in selected_specs:
                spec_value = random.choice(spec_values)
                GoodsSpec.objects.create(
                    goods=goods,
                    spec_name=spec_name,
                    spec_value=spec_value
                )
            break
    else:
        # 默认规格
        num_specs = random.randint(2, 3)
        for _ in range(num_specs):
            spec_name = random.choice(['颜色', '尺寸', '规格', '型号'])
            spec_value = random.choice(['标准款', '升级款', '豪华版'])
            GoodsSpec.objects.create(
                goods=goods,
                spec_name=spec_name,
                spec_value=spec_value
            )

def create_ecommerce_params(goods):
    """创建电商商品参数"""
    category_name = goods.category.category_name
    
    param_templates = {
        '手机': [
            ('品牌', lambda: random.choice(ECOMMERCE_BRANDS['手机数码'])),
            ('型号', lambda: f"MO-{random.randint(1000, 9999)}"),
            ('屏幕尺寸', lambda: f"{random.choice([5.8, 6.1, 6.5, 6.7])}英寸"),
            ('电池容量', lambda: f"{random.choice([4000, 4500, 5000, 5500])}mAh"),
            ('摄像头', lambda: f"{random.choice([4800, 5000, 6400])}万像素"),
            ('操作系统', lambda: random.choice(['Android 12', 'Android 13', 'iOS 15', 'iOS 16'])),
        ],
        '笔记本': [
            ('品牌', lambda: random.choice(ECOMMERCE_BRANDS['电脑办公'])),
            ('CPU型号', lambda: random.choice(['i5-1135G7', 'i7-1165G7', 'R5-5500U', 'R7-5800H'])),
            ('内存类型', lambda: random.choice(['DDR4', 'LPDDR4', 'LPDDR5'])),
            ('硬盘类型', lambda: random.choice(['SSD', 'NVMe SSD'])),
            ('屏幕分辨率', lambda: random.choice(['1920x1080', '2560x1440', '2880x1800'])),
            ('重量', lambda: f"{random.uniform(1.0, 3.0):.1f}kg"),
        ],
        '空调': [
            ('品牌', lambda: random.choice(ECOMMERCE_BRANDS['家用电器'])),
            ('制冷量', lambda: f"{random.randint(3200, 7200)}W"),
            ('制热量', lambda: f"{random.randint(3500, 8000)}W"),
            ('噪音值', lambda: f"{random.randint(20, 45)}dB"),
            ('适用面积', lambda: f"{random.randint(10, 50)}㎡"),
            ('电源', lambda: "220V/50Hz"),
        ],
        '运动鞋': [
            ('品牌', lambda: random.choice(ECOMMERCE_BRANDS['服装鞋帽'])),
            ('材质', lambda: random.choice(['真皮', '合成革', '网面', '帆布'])),
            ('鞋底材质', lambda: random.choice(['橡胶底', 'EVA底', 'PU底'])),
            ('产地', lambda: random.choice(['中国', '越南', '印度尼西亚', '泰国'])),
        ],
        '护肤': [
            ('品牌', lambda: random.choice(ECOMMERCE_BRANDS['美妆个护'])),
            ('保质期', lambda: f"{random.randint(2, 5)}年"),
            ('产地', lambda: random.choice(['中国', '日本', '韩国', '法国', '美国'])),
            ('适用年龄', lambda: random.choice(['18-25岁', '25-35岁', '35-45岁', '45岁以上'])),
        ]
    }
    
    # 匹配分类
    for key in param_templates:
        if key in category_name:
            num_params = random.randint(3, 6)
            selected_params = random.sample(param_templates[key], min(num_params, len(param_templates[key])))
            
            for param_name, param_func in selected_params:
                param_value = param_func()
                GoodsParam.objects.create(
                    goods=goods,
                    param_name=param_name,
                    param_value=param_value
                )
            break
    else:
        # 默认参数
        num_params = random.randint(3, 4)
        for _ in range(num_params):
            param_name = random.choice(['品牌', '产地', '保修期', '材质'])
            param_value = random.choice(['中国品牌', '进口商品', '1年保修', '优质材料'])
            GoodsParam.objects.create(
                goods=goods,
                param_name=param_name,
                param_value=param_value
            )
