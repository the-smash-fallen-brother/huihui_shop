
from rest_framework import serializers
from .models import Comment, CommentImage
from apps.accounts.models import User
from apps.goods.models import Goods
from apps.orders.models import Order

class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImage
        fields = ['image_id', 'image_url']

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
        return {
            'user_id': user.user_id,
            'username': user.username,
            'avatar_url': user.avatar_url
        }

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['goods', 'order', 'content', 'rating']
        extra_kwargs = {
            'rating': {'required': True}
        }