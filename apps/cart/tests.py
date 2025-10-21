from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from apps.cart.models import ShoppingCart
from apps.goods.models import Goods, GoodsCategory

User = get_user_model()

class ShoppingCartTestCase(APITestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            mobile='13800138000'
        )
        
        # 创建测试商品分类
        self.category = GoodsCategory.objects.create(
            category_name='测试分类',
            category_level=1
        )
        
        # 创建测试商品
        self.goods = Goods.objects.create(
            category=self.category,
            goods_name='测试商品',
            goods_price=100.00,
            market_price=120.00,
            cost_price=80.00,
            goods_desc='测试商品描述',
            goods_cover_img='http://example.com/image.jpg',
            goods_stock=100,
            goods_status=1
        )
        
        # 获取JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_cart_item_with_authenticated_user(self):
        """测试认证用户创建购物车项"""
        data = {
            'goods': self.goods.goods_id,
            'goods_num': 2
        }
        
        response = self.client.post('/cart/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['goods'], self.goods.goods_id)
        self.assertEqual(response.data['goods_num'], 2)
        
        # 验证数据库中的记录
        cart_item = ShoppingCart.objects.get(user=self.user, goods=self.goods)
        self.assertEqual(cart_item.goods_num, 2)

    def test_create_cart_item_without_user_field(self):
        """测试创建购物车项时不传递用户字段"""
        data = {
            'goods': self.goods.goods_id,
            'goods_num': 1
        }
        
        response = self.client.post('/cart/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], self.user.id)
        
        # 验证数据库中的记录
        cart_item = ShoppingCart.objects.get(user=self.user, goods=self.goods)
        self.assertEqual(cart_item.user, self.user)

    def test_user_cannot_access_other_users_cart(self):
        """测试用户不能访问其他用户的购物车"""
        # 创建另一个用户
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123',
            mobile='13800138001'
        )
        
        # 为其他用户创建购物车项
        other_cart_item = ShoppingCart.objects.create(
            user=other_user,
            goods=self.goods,
            goods_num=3
        )
        
        # 尝试访问其他用户的购物车项应该失败
        response = self.client.get(f'/cart/{other_cart_item.cart_id}/')
        self.assertEqual(response.status_code, 404)
        
        # 尝试更新其他用户的购物车项应该失败
        response = self.client.put(f'/cart/{other_cart_item.cart_id}/', {'goods_num': 5})
        self.assertEqual(response.status_code, 404)

    def test_increase_quantity_when_item_exists(self):
        """测试当商品已存在时增加数量"""
        # 先创建一个购物车项
        cart_item = ShoppingCart.objects.create(
            user=self.user,
            goods=self.goods,
            goods_num=2
        )
        
        # 再次添加同一商品
        data = {
            'goods': self.goods.goods_id,
            'goods_num': 3
        }
        
        response = self.client.post('/cart/', data, format='json')
        self.assertEqual(response.status_code, 200)  # 应该是更新而不是创建
        
        # 验证数量已增加
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.goods_num, 5)

    def test_cart_item_validation(self):
        """测试购物车项验证"""
        # 测试商品数量为0的情况
        data = {
            'goods': self.goods.goods_id,
            'goods_num': 0
        }
        
        response = self.client.post('/cart/', data, format='json')
        self.assertEqual(response.status_code, 400)