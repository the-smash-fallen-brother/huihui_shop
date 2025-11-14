
from rest_framework import serializers
from .models import Comment, CommentImage
from apps.accounts.models import User
from apps.goods.models import Goods
from apps.orders.models import Order

class CommentImageSerializer(serializers.ModelSerializer):
    image_url_full = serializers.SerializerMethodField()
    
    class Meta:
        model = CommentImage
        fields = ['image_id', 'image_url', 'image_url_full']
    
    def get_image_url_full(self, obj):
        if obj.image_url:
            # 构建完整的HTTP URL
            base_url = "http://localhost:8000"
            from django.conf import settings
            # 评论图片现在存储在comment_images目录下
            return f"{base_url}{settings.MEDIA_URL}{obj.image_url}"
        return None

class CommentSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    images = CommentImageSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['comment_id', 'user', 'user_info', 'goods', 'order',
                 'content', 'rating', 'images', 'reply_content',
                 'reply_time', 'comment_time']
        extra_kwargs = {
            'user': {'read_only': True},
            'comment_id': {'read_only': True},
            'comment_time': {'read_only': True}
        }

    def get_user_info(self, obj):
        user = obj.user
        from django.conf import settings
        
        if user.avatar:
            # 构建完整的HTTP URL (开发环境默认使用localhost:8000)
            base_url = "http://localhost:8000"
            # user.avatar.name 只返回相对路径，不需要重复添加MEDIA_URL
            avatar_url = f"{base_url}{settings.MEDIA_URL}{user.avatar.name}"
        else:
            # 使用默认头像或null
            avatar_url = None
            
        return {
            'user_id': user.user_id,
            'username': user.username,
            'avatar_url': avatar_url
        }

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['goods', 'order', 'content', 'rating']
        extra_kwargs = {
            'rating': {'required': True},
            'user': {'read_only': True}  # 设置为只读，由视图自动设置
        }