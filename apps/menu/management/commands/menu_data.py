# apps/menu/management/commands/generate_menus.py
from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from apps.menu.models import MainMenu, SubMenu  # 修正导入路径

class Command(BaseCommand):
    help = '生成菜单测试数据'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='清除现有菜单数据')
        parser.add_argument('--status', type=int, default=1, choices=[0, 1], help='菜单状态(0-禁用 1-启用)')

    def handle(self, *args, **options):
        clear = options.get('clear')
        status = options.get('status')

        if clear:
            SubMenu.objects.all().delete()
            MainMenu.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('菜单数据已清除'))

        self.stdout.write('开始生成菜单测试数据...')

        # 创建主菜单和子菜单
        menus_created = self.create_menus(status)
        
        self.stdout.write(self.style.SUCCESS(
            f'成功生成 {menus_created["main_menus"]} 个主菜单和 {menus_created["sub_menus"]} 个子菜单'
        ))

    def create_menus(self, status):
        """创建菜单数据"""
        # 一级分类作为主菜单
        main_categories = [
            {'name': '手机数码', 'icon': '📱', 'url': '/digital'},
            {'name': '电脑办公', 'icon': '💻', 'url': '/computer'},
            {'name': '家用电器', 'icon': '🏠', 'url': '/appliance'},
            {'name': '服装鞋帽', 'icon': '👕', 'url': '/clothing'},
            {'name': '美妆个护', 'icon': '💄', 'url': '/beauty'},
            {'name': '食品生鲜', 'icon': '🍎', 'url': '/food'},
            {'name': '运动户外', 'icon': '⚽', 'url': '/sports'},
            {'name': '家居家装', 'icon': '🛋️', 'url': '/furniture'},
            {'name': '母婴玩具', 'icon': '🧸', 'url': '/baby'},
            {'name': '图书文具', 'icon': '📚', 'url': '/books'}
        ]

        main_menus_count = 0
        sub_menus_count = 0

        for i, cat_data in enumerate(main_categories):
            # 创建主菜单
            main_menu = MainMenu.objects.create(
                menu_name=cat_data['name'],
                menu_url=cat_data['url'],
                menu_icon=cat_data['icon'],
                sort_order=i * 10,
                status=bool(status)
            )
            main_menus_count += 1

            # 为每个主菜单创建子菜单
            sub_categories = self.get_sub_categories(cat_data['name'])
            sub_menus_created = self.create_sub_menus(main_menu, sub_categories, status)
            sub_menus_count += sub_menus_created

        return {
            'main_menus': main_menus_count,
            'sub_menus': sub_menus_count
        }

    def get_sub_categories(self, main_category):
        """根据一级分类获取二级分类"""
        sub_categories_map = {
            '手机数码': [
                {'name': '智能手机', 'url': '/digital/smartphone', 'icon': '📱'},
                {'name': '平板电脑', 'url': '/digital/tablet', 'icon': '📟'},
                {'name': '智能手表', 'url': '/digital/smartwatch', 'icon': '⌚'},
                {'name': '耳机音箱', 'url': '/digital/audio', 'icon': '🎧'}
            ],
            '电脑办公': [
                {'name': '笔记本电脑', 'url': '/computer/laptop', 'icon': '💻'},
                {'name': '台式电脑', 'url': '/computer/desktop', 'icon': '🖥️'},
                {'name': '办公设备', 'url': '/computer/office', 'icon': '🖨️'},
                {'name': '电脑配件', 'url': '/computer/accessories', 'icon': '🖱️'}
            ],
            '家用电器': [
                {'name': '大家电', 'url': '/appliance/major', 'icon': '📺'},
                {'name': '厨房电器', 'url': '/appliance/kitchen', 'icon': '🍳'},
                {'name': '生活电器', 'url': '/appliance/life', 'icon': '🧹'},
                {'name': '个人护理', 'url': '/appliance/personal', 'icon': '💇'}
            ],
            '服装鞋帽': [
                {'name': '男装', 'url': '/clothing/men', 'icon': '👔'},
                {'name': '女装', 'url': '/clothing/women', 'icon': '👗'},
                {'name': '童装', 'url': '/clothing/kids', 'icon': '👶'},
                {'name': '鞋类', 'url': '/clothing/shoes', 'icon': '👟'}
            ],
            '美妆个护': [
                {'name': '护肤', 'url': '/beauty/skincare', 'icon': '💆'},
                {'name': '彩妆', 'url': '/beauty/makeup', 'icon': '💄'},
                {'name': '香水', 'url': '/beauty/perfume', 'icon': '🌸'},
                {'name': '美发', 'url': '/beauty/hair', 'icon': '💇'}
            ],
            '食品生鲜': [
                {'name': '休闲食品', 'url': '/food/snacks', 'icon': '🍿'},
                {'name': '生鲜果蔬', 'url': '/food/fresh', 'icon': '🍎'},
                {'name': '酒水饮料', 'url': '/food/drinks', 'icon': '🍷'},
                {'name': '粮油调味', 'url': '/food/grocery', 'icon': '🍚'}
            ],
            '运动户外': [
                {'name': '运动鞋服', 'url': '/sports/apparel', 'icon': '👟'},
                {'name': '体育器材', 'url': '/sports/equipment', 'icon': '⚽'},
                {'name': '户外装备', 'url': '/sports/outdoor', 'icon': '🏕️'},
                {'name': '健身器材', 'url': '/sports/fitness', 'icon': '💪'}
            ],
            '家居家装': [
                {'name': '家具', 'url': '/furniture/furniture', 'icon': '🛏️'},
                {'name': '家纺', 'url': '/furniture/textile', 'icon': '🛋️'},
                {'name': '家居装饰', 'url': '/furniture/decor', 'icon': '🖼️'},
                {'name': '厨房用品', 'url': '/furniture/kitchenware', 'icon': '🔪'}
            ],
            '母婴玩具': [
                {'name': '奶粉辅食', 'url': '/baby/formula', 'icon': '🍼'},
                {'name': '母婴用品', 'url': '/baby/supplies', 'icon': '🧴'},
                {'name': '童装童鞋', 'url': '/baby/clothing', 'icon': '👕'},
                {'name': '玩具', 'url': '/baby/toys', 'icon': '🧸'}
            ],
            '图书文具': [
                {'name': '图书', 'url': '/books/books', 'icon': '📚'},
                {'name': '文具', 'url': '/books/stationery', 'icon': '✏️'},
                {'name': '办公用品', 'url': '/books/office', 'icon': '📎'},
                {'name': '电子书', 'url': '/books/ebook', 'icon': '📱'}
            ]
        }
        return sub_categories_map.get(main_category, [])

    def create_sub_menus(self, main_menu, sub_categories, status):
        """为指定主菜单创建子菜单"""
        sub_menus_count = 0
        
        for j, sub_data in enumerate(sub_categories):
            # 随机决定菜单类型（80%普通菜单，20%功能菜单）
            menu_type = random.choices([1, 2], weights=[8, 2])[0]
            
            sub_menu = SubMenu.objects.create(
                menu=main_menu,
                sub_menu_name=sub_data['name'],
                sub_menu_type=menu_type,
                sub_menu_url=sub_data['url'],
                sub_menu_icon=sub_data['icon'],
                sort_order=j * 5,
                status=bool(status)
            )
            sub_menus_count += 1

        return sub_menus_count