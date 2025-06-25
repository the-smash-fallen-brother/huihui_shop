from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from apps.goods.models import GoodsCategory, Goods, GoodsSpec, GoodsParam
from apps.goods.serializers import (
    GoodsCategorySerializer, 
    GoodsSerializer, 
    GoodsDetailSerializer,
    GoodsSpecSerializer,
    GoodsParamSerializer
)

class GoodsCategoryListView(generics.ListAPIView):
    """
    商品分类列表接口
    GET /goods/categories/
    """
    queryset = GoodsCategory.objects.filter(status=True)
    serializer_class = GoodsCategorySerializer
    permission_classes = [AllowAny]


class GoodsListView(generics.ListAPIView):
    """
    商品列表接口
    GET /goods/list/
    """
    queryset = Goods.objects.filter(goods_status=1)
    serializer_class = GoodsSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category_id']
    search_fields = ['goods_name']
    ordering_fields = ['goods_price', 'goods_sales']
    ordering = ['-create_time']


class GoodsDetailView(generics.RetrieveAPIView):
    """
    商品详情接口
    GET /goods/detail/{goods_id}/
    """
    queryset = Goods.objects.filter(goods_status=1)
    serializer_class = GoodsDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'goods_id'


class GoodsHotView(generics.ListAPIView):
    """
    热销商品接口
    GET /goods/hot/
    """
    queryset = Goods.objects.filter(goods_status=1).order_by('-goods_sales')[:10]
    serializer_class = GoodsSerializer
    permission_classes = [AllowAny]


class GoodsNewView(generics.ListAPIView):
    """
    新品上架接口
    GET /goods/new/
    """
    queryset = Goods.objects.filter(goods_status=1).order_by('-create_time')[:10]
    serializer_class = GoodsSerializer
    permission_classes = [AllowAny]


class GoodsSpecView(generics.ListAPIView):
    """
    商品规格接口
    GET /goods/{goods_id}/specs/
    """
    serializer_class = GoodsSpecSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        goods_id = self.kwargs['goods_id']
        return GoodsSpec.objects.filter(goods_id=goods_id)


class GoodsParamView(generics.ListAPIView):
    """
    商品参数接口
    GET /goods/{goods_id}/params/
    """
    serializer_class = GoodsParamSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        goods_id = self.kwargs['goods_id']
        return GoodsParam.objects.filter(goods_id=goods_id)

class GoodsSearchView(generics.ListAPIView):
    """
    商品搜索接口
    GET /goods/search/
    
    参数：
    - q: 搜索关键词（匹配商品名称和描述）
    - min_price: 最低价格
    - max_price: 最高价格
    - category: 分类ID
    - status: 商品状态（1-上架，0-下架）
    - ordering: 排序字段（goods_price, -goods_price, goods_sales, -goods_sales, create_time, -create_time）
    
    示例：
    /goods/search/?q=手机&min_price=1000&max_price=5000&category=1&status=1&ordering=-goods_sales
    """
    serializer_class = GoodsSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # 配置过滤字段（与GoodsListView保持一致）
    filterset_fields = ['category_id', 'goods_status']
    search_fields = ['goods_name', 'goods_desc']
    ordering_fields = ['goods_price', 'goods_sales', 'create_time']
    ordering = ['-goods_sales']  # 默认按销量降序

    def get_queryset(self):
        queryset = Goods.objects.all()
        
        # 获取查询参数
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        # 自定义价格区间过滤（因为DjangoFilterBackend不支持范围过滤）
        if min_price:
            queryset = queryset.filter(goods_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(goods_price__lte=max_price)
            
        return queryset

    def list(self, request, *args, **kwargs):
        # 重写list方法以返回自定义响应格式（与现有接口风格一致）
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })


