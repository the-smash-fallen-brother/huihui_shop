from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.utils import timezone
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
    authentication_classes = []  # 禁用认证


class GoodsNewView(generics.ListAPIView):
    """
    新品上架接口
    GET /goods/new/
    """
    queryset = Goods.objects.filter(goods_status=1).order_by('-create_time')[:10]
    serializer_class = GoodsSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # 禁用认证


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


class GoodsRecommendView(generics.ListAPIView):
    """
    推荐商品接口
    GET /goods/recommend/
    
    参数：
    - type: 推荐类型（rating-按评分推荐，comments-按评论数推荐，sales-按销量推荐，默认rating）
    - limit: 返回数量限制（默认10个）
    
    示例：
    /goods/recommend/                    # 默认按评分推荐
    /goods/recommend/?type=rating      # 按评分推荐
    /goods/recommend/?type=comments    # 按评论数推荐
    /goods/recommend/?type=sales       # 按销量推荐
    /goods/recommend/?type=rating&limit=5  # 推荐5个高评分商品
    """
    serializer_class = GoodsSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # 禁用认证

    def get_queryset(self):
        # 获取参数
        recommend_type = self.request.query_params.get('type', 'rating')
        limit = int(self.request.query_params.get('limit', 10))
        
        # 基础查询：只查询上架商品
        queryset = Goods.objects.filter(goods_status=1)
        
        if recommend_type == 'comments':
            # 按评论数推荐
            queryset = queryset.annotate(
                comment_count=models.Count('comments')
            ).filter(comment_count__gt=0).order_by('-comment_count')
            
            # 如果没有评论，返回空结果
            if not queryset.exists():
                return Goods.objects.none()
                
        elif recommend_type == 'sales':
            # 按销量推荐
            queryset = queryset.order_by('-goods_sales')
            
        else:
            # 按评分推荐（默认）
            queryset = queryset.annotate(
                avg_rating=models.Avg('comments__rating'),
                comment_count=models.Count('comments')
            ).filter(comment_count__gt=0).order_by('-avg_rating', '-comment_count')
            
            # 如果没有评论，改为按销量推荐
            if not queryset.exists():
                queryset = Goods.objects.filter(goods_status=1).order_by('-goods_sales')
        
        return queryset[:limit]


class GoodsImageUploadView(generics.UpdateAPIView):
    """
    商品图片上传接口
    POST /goods/{goods_id}/upload-images/
    
    用于上传商品封面图和轮播图文件
    需要认证权限，仅限管理员使用
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'goods_id'
    
    def update(self, request, *args, **kwargs):
        goods = self.get_object()
        
        # 处理封面图上传
        if 'goods_cover_img_file' in request.FILES:
            goods.goods_cover_img_file = request.FILES['goods_cover_img_file']
            goods.save()
        
        # 处理轮播图上传
        carousel_files = request.FILES.getlist('goods_carousel_files')
        if carousel_files:
            # 保存轮播图文件信息
            carousel_files_info = []
            for idx, file in enumerate(carousel_files):
                # 为每个轮播图生成唯一文件名
                file_extension = file.name.split('.')[-1]
                file_name = f"carousel_{goods.goods_id}_{idx + 1}.{file_extension}"
                
                # 保存文件
                goods.goods_carousel_files.append({
                    'file_name': file_name,
                    'original_name': file.name,
                    'size': file.size,
                    'upload_time': timezone.now().isoformat()
                })
                
                # 这里可以根据需要实际保存文件到指定目录
                # 由于使用了ImageField，Django会自动处理文件保存
                
            goods.save()
        
        # 返回更新后的商品信息
        serializer = self.get_serializer(goods)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FlashSaleGoodsListView(generics.ListAPIView):
    """
    秒杀商品列表接口
    GET /goods/flash-sale/
    
    返回当前正在进行的秒杀商品
    """
    serializer_class = GoodsSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # 禁用认证

    def get_queryset(self):
        current_time = timezone.now()
        # 查询正在进行中的秒杀商品
        queryset = Goods.objects.filter(
            is_flash_sale=True,
            goods_status=1,
            flash_sale_start_time__lte=current_time,
            flash_sale_end_time__gte=current_time,
            flash_sale_stock__gt=0
        ).order_by('flash_sale_end_time')  # 按结束时间升序，即将结束的排在前面
        return queryset


class FlashSaleGoodsDetailView(generics.RetrieveAPIView):
    """
    秒杀商品详情接口
    GET /goods/flash-sale/{goods_id}/
    
    返回指定秒杀商品的详细信息
    """
    serializer_class = GoodsDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'goods_id'

    def get_queryset(self):
        current_time = timezone.now()
        # 查询正在进行中的秒杀商品
        queryset = Goods.objects.filter(
            goods_id=self.kwargs['goods_id'],
            is_flash_sale=True,
            goods_status=1,
            flash_sale_start_time__lte=current_time,
            flash_sale_end_time__gte=current_time
        )
        return queryset


class UpcomingFlashSaleView(generics.ListAPIView):
    """
    即将开始的秒杀商品接口
    GET /goods/upcoming-flash-sale/
    
    返回即将开始的秒杀商品（未来24小时内）
    """
    serializer_class = GoodsSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # 禁用认证

    def get_queryset(self):
        current_time = timezone.now()
        # 查询未来24小时内即将开始的秒杀商品
        queryset = Goods.objects.filter(
            is_flash_sale=True,
            goods_status=1,
            flash_sale_start_time__gt=current_time,
            flash_sale_start_time__lte=current_time + timezone.timedelta(hours=24),
            flash_sale_stock__gt=0
        ).order_by('flash_sale_start_time')  # 按开始时间升序，即将开始的排在前面
        return queryset


