from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import User, UserAddress, UserFavorite
from apps.goods.models import Goods
from apps.accounts.serializers import (
    UserSerializer, 
    UserAddressSerializer,
    UserFavoriteSerializer
)

class RegisterView(APIView):
    """用户注册"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # 合并请求体和URL查询参数
            data = {**request.data, **request.query_params.dict()}
            serializer = UserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class LoginView(APIView):
    """用户登录"""
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            return Response(
                {'error': '用户名或密码错误'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user_id': user.user_id,
            'username': user.username,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
# logout退出登录
class LogoutView(APIView):
    """用户退出登录"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': '退出成功'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST          
            )
        


class UserInfoView(APIView):
    """用户信息"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(
            request.user, 
            data=request.data, 
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserAddressView(APIView):
    """地址管理"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取地址列表"""
        addresses = request.user.addresses.all()
        serializer = UserAddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def get_default(self, request):
        """获取默认地址"""
        address = request.user.addresses.filter(is_default=True).first()
        if not address:
            return Response(
                {'error': '未设置默认地址'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserAddressSerializer(address)
        return Response(serializer.data)

    def post(self, request):
        """添加新地址"""
        serializer = UserAddressSerializer(
            data=request.data,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserPasswordView(APIView):
    """密码修改"""
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response(
                {'error': '原密码错误'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user.set_password(new_password)
        user.save()
        return Response({'message': '密码修改成功'})




class UserAddressDetailView(APIView):
    """地址详情管理"""
    permission_classes = [permissions.IsAuthenticated]

    def get_address(self, address_id):
        try:
            return self.request.user.addresses.get(pk=address_id)
        except UserAddress.DoesNotExist:
            return None

    def get(self, request, address_id):
        """获取地址详情"""
        address = self.get_address(address_id)
        if not address:
            return Response(
                {'error': '地址不存在'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserAddressSerializer(address)
        return Response(serializer.data)

    def put(self, request, address_id):
        """更新地址"""
        address = self.get_address(address_id)
        if not address:
            return Response(
                {'error': '地址不存在'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UserAddressSerializer(
            address, 
            data=request.data, 
            partial=True,
            context={'user': request.user}  # 确保传递用户上下文
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def post(self, request, address_id):
        """设置默认地址"""
        address = self.get_address(address_id)
        if not address:
            return Response(
                {'error': '地址不存在'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 将用户所有地址设为非默认
        request.user.addresses.filter(is_default=True).update(is_default=False)
        
        # 将当前地址设为默认
        address.is_default = True
        address.save()
        
        serializer = UserAddressSerializer(address)
        return Response(serializer.data)

    def delete(self, request, address_id):
        """删除地址"""
        address = self.get_address(address_id)
        if not address:
            return Response(
                {'error': '地址不存在'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserFavoriteView(APIView):
    """用户收藏管理"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取用户收藏列表"""
        favorites = UserFavorite.objects.filter(user=request.user)
        serializer = UserFavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        """添加收藏"""
        goods_id = request.data.get('goods_id')
        if not goods_id:
            return Response(
                {'error': '缺少goods_id参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            goods = Goods.objects.get(pk=goods_id)
        except Goods.DoesNotExist:
            return Response(
                {'error': '商品不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        favorite, created = UserFavorite.objects.get_or_create(
            user=request.user,
            goods=goods
        )
        
        if not created:
            return Response(
                {'message': '商品已在收藏中'},
                status=status.HTTP_200_OK
            )
            
        serializer = UserFavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, goods_id):
        """删除收藏"""
        try:
            favorite = UserFavorite.objects.get(
                user=request.user,
                goods_id=goods_id
            )
            favorite.delete()
            return Response({'message': '收藏删除成功'})
        except UserFavorite.DoesNotExist:
            return Response(
                {'error': '收藏不存在'},
                status=status.HTTP_404_NOT_FOUND
            )

class UserFavoriteCheckView(APIView):
    """检查收藏状态"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """检查商品是否被收藏"""
        goods_id = request.query_params.get('goods_id')
        if not goods_id:
            return Response(
                {'error': '缺少goods_id参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_favorite = UserFavorite.objects.filter(
            user=request.user,
            goods_id=goods_id
        ).exists()
        
        return Response({'is_favorite': is_favorite})