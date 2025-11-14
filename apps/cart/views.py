from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.cart.models import ShoppingCart
from apps.cart.serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer
import logging

logger = logging.getLogger(__name__)


class ShoppingCartView(generics.ListCreateAPIView):
    """
    购物车接口
    GET /cart/ - 获取购物车列表
    POST /cart/ - 添加商品到购物车
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        # 确保只返回当前用户的购物车项，并按创建时间排序以避免分页警告
        return ShoppingCart.objects.filter(user=self.request.user).order_by('create_time')

    def perform_create(self, serializer):
        # 在保存前自动关联当前用户，不依赖前端传递的user_id
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        # 不使用前端传递的任何user信息，确保使用认证用户
        data = request.data.copy()
        
        # 验证用户认证状态
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': '用户未认证'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # 移除可能存在的user字段，确保使用认证用户
        if 'user' in data:
            del data['user']
        
        # 检查必需的商品ID
        goods_id = data.get('goods')
        if not goods_id:
            return Response(
                {'error': '缺少商品ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 检查商品是否已在购物车
        cart_item = ShoppingCart.objects.filter(
            user=request.user, 
            goods_id=goods_id
        ).first()
        
        if cart_item:
            # 如果商品已存在，增加数量
            goods_num = int(data.get('goods_num', 1))
            cart_item.goods_num += goods_num
            cart_item.save()
            serializer = ShoppingCartSerializer(cart_item)
            
            return Response(serializer.data)
        
        # 创建新的购物车项
        serializer = ShoppingCartSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            # 使用perform_create方法确保正确关联用户
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    购物车详情接口
    GET /cart/{cart_id}/ - 获取购物车项详情
    PUT /cart/{cart_id}/ - 更新购物车项
    DELETE /cart/{cart_id}/ - 删除购物车项
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ShoppingCartDetailSerializer
    lookup_field = 'cart_id'

    def get_queryset(self):
        # 确保用户只能访问自己的购物车项
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        # 根据操作类型选择不同的序列化器
        if self.request.method in ['PUT', 'PATCH']:
            return ShoppingCartDetailSerializer
        return ShoppingCartSerializer

    def perform_update(self, serializer):
        # 更新时确保用户信息不变
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        # 重写update方法以提供更详细的错误信息
        logger.info(f"购物车更新请求: cart_id={kwargs.get('cart_id')}, data={request.data}")
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        logger.info(f"获取到购物车实例: {instance}")
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            logger.info(f"序列化器验证通过，准备保存数据")
            self.perform_update(serializer)
            logger.info(f"购物车更新成功: {serializer.data}")
            return Response(serializer.data)
        except serializers.ValidationError as e:
            # 记录详细的验证错误信息
            logger.error(f"序列化器验证失败: {e.detail}")
            return Response(
                {'error': '验证失败', 'details': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # 记录详细错误信息
            logger.error(f"购物车更新失败: {str(e)}", exc_info=True)
            
            # 返回更详细的错误信息
            return Response(
                {'error': f'更新失败: {str(e)}', 'detail': '请检查商品状态和库存'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ShoppingCartCheckAllView(generics.GenericAPIView):
    """
    购物车全选/取消全选接口
    POST /cart/check/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 验证用户认证状态
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': '用户未认证'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        selected = request.data.get('selected', True)
        # 只更新当前用户的购物车项
        ShoppingCart.objects.filter(user=request.user).update(selected=selected)
        return Response({'message': '操作成功'})


class ShoppingCartClearView(generics.GenericAPIView):
    """
    清空购物车接口
    DELETE /cart/clear/
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        # 验证用户认证状态
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': '用户未认证'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        # 只删除当前用户的购物车项
        ShoppingCart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)