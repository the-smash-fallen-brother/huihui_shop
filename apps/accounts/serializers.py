from rest_framework import serializers
from .models import User, UserAddress, UserFavorite
from apps.goods.models import Goods
from apps.goods.serializers import GoodsSimpleSerializer

class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'mobile', 'email',
            'gender', 'birthday', 'avatar', 'avatar_url', 'status', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': False},  # 改为非必填
            'mobile': {'required': True},
            'username': {'required': True}
        }
    
    def get_avatar_url(self, obj):
        """获取头像的完整URL"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None

    def create(self, validated_data):
        """创建用户并设置密码"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            mobile=validated_data['mobile'],
            password=validated_data['password']
        )
        return user

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            'address_id', 'receiver_name', 'receiver_mobile',
            'province', 'city', 'district', 'detailed_address',
            'is_default', 'create_time', 'update_time'
        ]
        read_only_fields = ['user', 'create_time']

    def validate(self, data):
        """验证数据有效性"""
        # 验证手机号格式
        if len(data.get('receiver_mobile', '')) != 11:
            raise serializers.ValidationError("手机号必须为11位")
        
        # 获取当前用户（从上下文中）
        user = self.context.get('user')
        if user and data.get('is_default', False):
            # 排除当前正在修改的地址（如果是更新操作）
            exclude_id = self.instance.address_id if self.instance else None
            if user.addresses.filter(is_default=True).exclude(pk=exclude_id).exists():
                raise serializers.ValidationError("已存在默认地址")
        
        return data

    def create(self, validated_data):
        """创建时自动关联当前用户"""
        validated_data['user'] = self.context['user']
        return super().create(validated_data)

class UserFavoriteSerializer(serializers.ModelSerializer):
    goods = GoodsSimpleSerializer(read_only=True)
    goods_id = serializers.PrimaryKeyRelatedField(
        queryset=Goods.objects.all(),
        write_only=True,
        source='goods'
    )

    class Meta:
        model = UserFavorite
        fields = ['id', 'goods', 'goods_id', 'created_time']
        read_only_fields = ['created_time']








class UserFavoriteSerializer(serializers.ModelSerializer):
    goods = GoodsSimpleSerializer(read_only=True)
    goods_id = serializers.PrimaryKeyRelatedField(
        queryset=Goods.objects.all(),
        write_only=True,
        source='goods'
    )

    class Meta:
        model = UserFavorite
        fields = ['id', 'goods', 'goods_id', 'created_time']
        read_only_fields = ['created_time']

    def validate(self, data):
        """验证用户是否已收藏该商品"""
        user = self.context['request'].user
        goods = data.get('goods')
        
        if UserFavorite.objects.filter(user=user, goods=goods).exists():
            raise serializers.ValidationError("该商品已在收藏中")
        
        return data

    def create(self, validated_data):
        """创建收藏记录"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)