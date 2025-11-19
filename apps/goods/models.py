from django.db import models

class GoodsCategory(models.Model):
    """
    商品分类表
    """
    CATEGORY_LEVEL_CHOICES = (
        (1, '一级分类'),
        (2, '二级分类')
    )
    
    category_id = models.AutoField(primary_key=True, verbose_name='分类ID')
    category_name = models.CharField(max_length=50, verbose_name='分类名称')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                             related_name='children', verbose_name='父分类')
    category_level = models.SmallIntegerField(choices=CATEGORY_LEVEL_CHOICES, verbose_name='分类等级')
    category_icon = models.CharField(max_length=255, blank=True, null=True, verbose_name='分类图标')
    sort_order = models.IntegerField(default=0, verbose_name='排序值')
    status = models.BooleanField(default=True, verbose_name='状态(0-禁用 1-启用)')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        app_label = 'goods'
        db_table = 'goods_category'
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'parent_id': self.parent_id if self.parent else None,
            'category_level': self.category_level,
            'status': self.status
        }.__str__()


class Goods(models.Model):
    """
    商品表
    """
    GOODS_STATUS_CHOICES = (
        (0, '下架'),
        (1, '上架')
    )
    
    goods_id = models.AutoField(primary_key=True, verbose_name='商品ID')
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='goods', verbose_name='商品分类')
    goods_name = models.CharField(max_length=100, verbose_name='商品名称')
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    market_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='市场价格')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='成本价格')
    goods_desc = models.TextField(verbose_name='商品描述')
    goods_cover_img = models.URLField(max_length=255, verbose_name='商品封面图')
    goods_cover_img_file = models.ImageField(upload_to='goods_img/cover/', null=True, blank=True, verbose_name='商品封面图文件')
    goods_carousel = models.JSONField(default=list, verbose_name='商品轮播图(JSON数组)')
    goods_carousel_files = models.JSONField(default=list, null=True, blank=True, verbose_name='商品轮播图文件列表')
    goods_stock = models.IntegerField(default=0, verbose_name='商品库存')
    goods_sales = models.IntegerField(default=0, verbose_name='商品销量')
    goods_status = models.SmallIntegerField(choices=GOODS_STATUS_CHOICES, default=1, verbose_name='商品状态')
    
    # 秒杀相关字段
    is_flash_sale = models.BooleanField(default=False, verbose_name='是否秒杀商品')
    flash_sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='秒杀价格')
    flash_sale_stock = models.IntegerField(default=0, verbose_name='秒杀库存')
    flash_sale_start_time = models.DateTimeField(null=True, blank=True, verbose_name='秒杀开始时间')
    flash_sale_end_time = models.DateTimeField(null=True, blank=True, verbose_name='秒杀结束时间')
    
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        app_label = 'goods'
        db_table = 'goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return {
            'goods_id': self.goods_id,
            'goods_name': self.goods_name,
            'goods_price': float(self.goods_price),
            'goods_status': self.goods_status,
            'goods_stock': self.goods_stock,
            'goods_sales': self.goods_sales
        }.__str__()


class GoodsSpec(models.Model):
    """
    商品规格表
    """
    spec_id = models.AutoField(primary_key=True, verbose_name='规格ID')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='specs', verbose_name='商品')
    spec_name = models.CharField(max_length=50, verbose_name='规格名称')
    spec_value = models.CharField(max_length=100, verbose_name='规格值')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        app_label = 'goods'
        db_table = 'goods_spec'
        verbose_name = '商品规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return {
            'spec_id': self.spec_id,
            'goods_id': self.goods_id,
            'spec_name': self.spec_name,
            'spec_value': self.spec_value
        }.__str__()


class GoodsParam(models.Model):
    """
    商品参数表
    """
    param_id = models.AutoField(primary_key=True, verbose_name='参数ID')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='params', verbose_name='商品')
    param_name = models.CharField(max_length=50, verbose_name='参数名')
    param_value = models.CharField(max_length=100, verbose_name='参数值')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        app_label = 'goods'
        db_table = 'goods_param'
        verbose_name = '商品参数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return {
            'param_id': self.param_id,
            'goods_id': self.goods_id,
            'param_name': self.param_name,
            'param_value': self.param_value
        }.__str__()


class GoodsCarousel(models.Model):
    """
    商品轮播图表
    """
    carousel_id = models.AutoField(primary_key=True, verbose_name='轮播图ID')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='carousel_images', verbose_name='商品')
    image = models.ImageField(upload_to='goods_img/carousel/', verbose_name='轮播图片')
    alt_text = models.CharField(max_length=200, blank=True, null=True, verbose_name='图片描述')
    sort_order = models.IntegerField(default=0, verbose_name='排序值')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        app_label = 'goods'
        db_table = 'goods_carousel'
        verbose_name = '商品轮播图'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', 'create_time']

    def __str__(self):
        return f"{self.goods.goods_name} - 轮播图{self.carousel_id}"


