# apps/accounts/management/commands/generate_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random
from faker import Faker
from django.conf import settings

fake = Faker('zh_CN')

class Command(BaseCommand):
    help = '生成用户测试数据（包含头像URL）'

    def add_arguments(self, parser):
        parser.add_argument('--number', '-n', type=int, default=15, help='要生成的用户数量')
        parser.add_argument('--clear', action='store_true', help='清除现有测试用户')
        parser.add_argument('--with-address', action='store_true', help='同时生成用户地址')
        parser.add_argument('--with-favorites', action='store_true', help='同时生成用户收藏')

    def handle(self, *args, **options):
        User = get_user_model()
        number = options['number']
        clear = options.get('clear')
        with_address = options.get('with_address')
        with_favorites = options.get('with_favorites')

        if clear:
            # 只删除普通测试用户，保留管理员用户
            User.objects.filter(is_staff=False, is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('测试用户数据已清除'))

        self.stdout.write(f'开始生成 {number} 个用户测试数据...')

        created_users = []
        for i in range(number):
            try:
                user = self.create_user(i)
                created_users.append(user)
                
                if with_address:
                    self.create_user_addresses(user)
                
                if (i + 1) % 5 == 0:
                    self.stdout.write(f'已生成 {i + 1} 个用户...')

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'生成用户时出错: {e}'))
                continue

        if with_favorites and created_users:
            self.create_user_favorites(created_users)

        self.stdout.write(self.style.SUCCESS(f'成功生成 {len(created_users)} 个用户测试数据'))

    def create_user(self, index):
        """创建单个用户"""
        User = get_user_model()
        
        # 生成唯一用户名和手机号
        username = f'testuser{index + 1:03d}'
        mobile = self.generate_unique_mobile()
        email = f'{username}@example.com'
        
        # 生成用户头像URL - 使用Unsplash Source
        avatar_url = self.generate_avatar_url()
        
        # 随机生成生日（18-60岁之间）
        birth_year = random.randint(1965, 2005)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        birthday = datetime(birth_year, birth_month, birth_day).date()
        
        # 随机生成最后登录时间（最近30天内）
        last_login_time = timezone.now() - timedelta(days=random.randint(0, 30))
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password='test123456',  # 统一测试密码
            mobile=mobile,
            gender=random.choice([0, 1, 2]),
            avatar_url=avatar_url,
            birthday=birthday,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            status=random.choices([0, 1], weights=[1, 9])[0],  # 90%概率正常状态
            last_login_time=last_login_time if random.choice([True, False]) else None,
            is_active=True
        )
        
        return user

    def generate_unique_mobile(self):
        """生成唯一的手机号"""
        User = get_user_model()
        while True:
            # 生成以1开头的11位手机号
            mobile = f'1{random.randint(3, 9)}{random.randint(100000000, 999999999):09d}'[:11]
            if not User.objects.filter(mobile=mobile).exists():
                return mobile

    def generate_avatar_url(self):
        """生成用户头像URL - 使用Unsplash Source"""
        # 多种头像风格选择
        avatar_styles = [
            'portrait', 'face', 'person', 'human', 'profile',
            'man', 'woman', 'boy', 'girl', 'people'
        ]
        
        style = random.choice(avatar_styles)
        width = height = random.choice([200, 300, 400, 500])
        
        # 使用Unsplash Source生成头像URL
        return f'https://source.unsplash.com/{width}x{height}/?{style}'

    def create_user_addresses(self, user):
        """为用户创建地址"""
        from apps.accounts.models import UserAddress
        
        # 每个用户创建1-3个地址
        num_addresses = random.randint(1, 3)
        
        provinces = ['北京市', '上海市', '广州市', '深圳市', '杭州市', '成都市', '武汉市', '南京市']
        cities = {
            '北京市': ['朝阳区', '海淀区', '东城区', '西城区'],
            '上海市': ['浦东新区', '徐汇区', '静安区', '黄浦区'],
            '广州市': ['天河区', '越秀区', '海珠区', '荔湾区'],
            '深圳市': ['南山区', '福田区', '罗湖区', '宝安区'],
            '杭州市': ['西湖区', '上城区', '下城区', '滨江区'],
            '成都市': ['锦江区', '青羊区', '武侯区', '成华区'],
            '武汉市': ['江岸区', '江汉区', '硚口区', '汉阳区'],
            '南京市': ['玄武区', '秦淮区', '建邺区', '鼓楼区']
        }
        
        streets = [
            '中山路', '人民路', '解放路', '建设路', '和平路',
            '长江路', '黄河路', '延安路', '北京路', '上海路'
        ]
        
        for i in range(num_addresses):
            province = random.choice(provinces)
            city = random.choice(cities[province])
            
            address = UserAddress.objects.create(
                user=user,
                receiver_name=fake.name(),
                receiver_mobile=self.generate_unique_mobile(),
                province=province,
                city=city,
                district=random.choice(['中心区', '新区', '开发区']),
                detailed_address=f'{random.choice(streets)}{random.randint(1, 999)}号',
                is_default=(i == 0)  # 第一个地址设为默认
            )

    def create_user_favorites(self, users):
        """为用户创建收藏"""
        from apps.accounts.models import UserFavorite
        from apps.goods.models import Goods
        
        goods_list = list(Goods.objects.all())
        if not goods_list:
            self.stdout.write(self.style.WARNING('没有商品数据，无法生成收藏记录'))
            return
        
        for user in users:
            # 每个用户收藏3-10个商品
            num_favorites = random.randint(3, 10)
            favorite_goods = random.sample(goods_list, min(num_favorites, len(goods_list)))
            
            for goods in favorite_goods:
                UserFavorite.objects.get_or_create(
                    user=user,
                    goods=goods,
                    defaults={'created_time': timezone.now() - timedelta(days=random.randint(1, 90))}
                )