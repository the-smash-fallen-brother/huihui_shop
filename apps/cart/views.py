
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.cart.models import ShoppingCart
from apps.cart.serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer

class ShoppingCartView(generics.ListCreateAPIView):
    """
    购物车接口
    GET /cart/ - 获取购物车列表
    POST /cart/ - 添加商品到购物车
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.user_id
        
        # 检查商品是否已在购物车
        cart_item = ShoppingCart.objects.filter(
            user=request.user, 
            goods_id=data['goods']
        ).first()
        
        if cart_item:
            cart_item.goods_num += int(data.get('goods_num', 1))
            cart_item.save()
            serializer = ShoppingCartSerializer(cart_item)
            return Response(serializer.data)
        
        serializer = ShoppingCartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
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
    serializer_class = ShoppingCartSerializer
    lookup_field = 'cart_id'

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class ShoppingCartCheckAllView(generics.GenericAPIView):
    """
    购物车全选/取消全选接口
    POST /cart/check/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        selected = request.data.get('selected', True)
        ShoppingCart.objects.filter(user=request.user).update(selected=selected)
        return Response({'message': '操作成功'})


class ShoppingCartClearView(generics.GenericAPIView):
    """
    清空购物车接口
    DELETE /cart/clear/
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        ShoppingCart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
