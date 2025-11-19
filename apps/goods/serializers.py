from rest_framework import serializers
from .models import GoodsCategory, Goods, GoodsSpec, GoodsParam

class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ['category_id', 'category_name', 'parent', 'category_level',
                 'category_icon', 'sort_order', 'status']

class GoodsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    flash_sale_start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    flash_sale_end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    goods_cover_img_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Goods
        fields = ['goods_id', 'goods_name', 'goods_price', 'market_price',
                 'goods_cover_img', 'goods_cover_img_file', 'goods_cover_img_file_url', 
                 'goods_carousel', 'goods_carousel_files', 'goods_sales', 'goods_status', 
                 'category_name', 'create_time', 'is_flash_sale', 'flash_sale_price',
                 'flash_sale_stock', 'flash_sale_start_time', 'flash_sale_end_time']
    
    def get_goods_cover_img_file_url(self, obj):
        if obj.goods_cover_img_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.goods_cover_img_file.url)
            return obj.goods_cover_img_file.url
        return None

class GoodsDetailSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer()
    specs = serializers.SerializerMethodField()
    params = serializers.SerializerMethodField()

    class Meta:
        model = Goods
        fields = '__all__'

    def get_specs(self, obj):
        specs = obj.specs.all()
        return GoodsSpecSerializer(specs, many=True).data

    def get_params(self, obj):
        params = obj.params.all()
        return GoodsParamSerializer(params, many=True).data

class GoodsSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsSpec
        fields = ['spec_id', 'spec_name', 'spec_value']

class GoodsParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsParam
        fields = ['param_id', 'param_name', 'param_value']

class GoodsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ['goods_id', 'goods_name', 'goods_price']