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
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # 检查商品是否存在
        from apps.goods.models import Goods
        try:
            goods = Goods.objects.get(goods_id=self.kwargs['goods_id'])
        except Goods.DoesNotExist:
            return Response({'error': '商品不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        # 即使没有评论也返回空列表
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })


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
    POST /reviews/ - 添加评论
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        # 自动设置用户ID
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        # 验证用户是否有权限评论该订单
        try:
            order = Order.objects.get(order_id=data['order'], user=request.user)
            if order.order_status != 4:  # 只有已完成订单可以评论
                return Response({'error': '只有已完成订单可以评论'}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({'error': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        comment = serializer.instance
        
        # 处理评论图片
        images = request.FILES.getlist('images')
        import os
        import uuid
        from datetime import datetime
        
        for i, image in enumerate(images):
            # 生成安全的文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            random_str = str(uuid.uuid4())[:8]
            file_ext = os.path.splitext(image.name)[1]  # 保留原文件扩展名
            safe_filename = f"comment_{timestamp}_{random_str}_{i}{file_ext}"
            
            # 重命名文件
            image.name = safe_filename
            
            CommentImage.objects.create(
                comment=comment,
                image_url=image  # 现在使用安全的文件名
            )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
