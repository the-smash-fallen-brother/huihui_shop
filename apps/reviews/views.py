from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.reviews.models import Comment, CommentImage
from apps.reviews.serializers import CommentSerializer, CommentCreateSerializer
from apps.orders.models import Order

class CommentListView(generics.ListAPIView):
    """
    商品评论接口
    GET /comments/goods/{goods_id}/ - 获取商品评论列表
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        goods_id = self.kwargs['goods_id']
        return Comment.objects.filter(goods_id=goods_id).order_by('-comment_time')


class UserCommentListView(generics.ListAPIView):
    """
    用户评论接口
    GET /comments/user/ - 获取用户评论列表
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user).order_by('-comment_time')


class CommentCreateView(generics.CreateAPIView):
    """
    创建评论接口
    POST /comments/ - 添加评论
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.user_id
        
        # 验证用户是否有权限评论该订单
        try:
            order = Order.objects.get(order_id=data['order'], user=request.user)
            if order.order_status != 4:  # 只有已完成订单可以评论
                return Response({'error': '只有已完成订单可以评论'}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({'error': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentCreateSerializer(data=data)
        if serializer.is_valid():
            comment = serializer.save()
            
            # 处理评论图片
            images = request.FILES.getlist('images')
            for image in images:
                CommentImage.objects.create(
                    comment=comment,
                    image_url=image  # 实际项目中需要上传到云存储并返回URL
                )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
