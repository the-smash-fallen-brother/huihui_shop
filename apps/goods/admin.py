from django.contrib import admin
from django.utils.html import format_html
from .models import GoodsCategory, Goods, GoodsSpec, GoodsParam, GoodsCarousel
# 定义内连类
class GoodsSpecInline(admin.TabularInline):
    """商品类型内联编辑"""
    model = GoodsSpec
    extra = 1
    fields = ('spec_name', 'spec_value')

class GoodsParamInline(admin.TabularInline):
    """商品参数内联编辑"""
    model = GoodsParam
    extra = 1
    fields = ('param_name', 'param_value')

class GoodsCarouselInline(admin.TabularInline):
    """商品轮播图内联编辑"""
    model = GoodsCarousel
    extra = 3
    fields = ('image', 'alt_text', 'sort_order', 'is_active')

class GoodsCategoryInline(admin.TabularInline):
    """二级分类内联编辑"""
    model = GoodsCategory
    fk_name = 'parent'  # 指定父关联字段
    extra = 1
    fields = ('category_name', 'category_level', 'category_icon', 'sort_order', 'status')
    ordering = ('sort_order',)
# 定义左侧菜单模型
@admin.register(GoodsCategory)
class GoodsCategoryAdmin(admin.ModelAdmin):
    """商品分类Admin配置"""
    list_display = ('category_name', 'parent_display', 'category_level_display', 
                   'icon_preview', 'sort_order', 'status_display', 'create_time')
    list_editable = ('sort_order',)
    list_filter = ('category_level', 'status', 'create_time')
    search_fields = ('category_name',)
    ordering = ('category_level', 'sort_order')
    inlines = [GoodsCategoryInline]  # 用于添加二级分类
    actions = ['enable_categories', 'disable_categories']
    
    # 自定义字段显示
    def parent_display(self, obj):
        return obj.parent.category_name if obj.parent else '一级分类'
    parent_display.short_description = '父分类'
    
    def category_level_display(self, obj):
        return obj.get_category_level_display()
    category_level_display.short_description = '分类等级'
    
    def status_display(self, obj):
        return '启用' if obj.status else '禁用'
    status_display.short_description = '状态'
    
    def icon_preview(self, obj):
        if obj.category_icon:
            return format_html('<img src="{}" height="30" />', obj.category_icon)
        return '-'
    icon_preview.short_description = '图标预览'
    
    # 批量操作
    def enable_categories(self, request, queryset):
        queryset.update(status=True)
    enable_categories.short_description = "启用所选分类"
    
    def disable_categories(self, request, queryset):
        queryset.update(status=False)
    disable_categories.short_description = "禁用所选分类"



@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('goods_id', 'goods_name', 'category', 'goods_price', 'goods_stock', 
                   'goods_sales', 'status_display', 'cover_image_preview', 'image_type_display', 'create_time')
    list_editable = ('goods_price', 'goods_stock')
    list_filter = ('goods_status', 'category', 'is_flash_sale', 'create_time')
    search_fields = ('goods_name', 'goods_desc')
    readonly_fields = ('goods_id',)
    inlines = [GoodsCarouselInline, GoodsSpecInline, GoodsParamInline]
    actions = ['enable_goods', 'disable_goods', 'set_flash_sale', 'remove_flash_sale']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('goods_name', 'category', 'goods_desc', 'goods_status')
        }),
        ('价格信息', {
            'fields': ('goods_price', 'market_price', 'cost_price', 'goods_stock', 'goods_sales')
        }),
        ('封面图片', {
            'fields': ('goods_cover_img_file',),
            'description': '上传商品封面图片'
        }),
        ('秒杀信息', {
            'fields': ('is_flash_sale', 'flash_sale_price', 'flash_sale_stock', 
                      'flash_sale_start_time', 'flash_sale_end_time'),
            'classes': ('collapse',),
            'description': '设置秒杀商品信息（勾选"是否秒杀商品"后，请填写以下字段）'
        }),
    )
    
    def status_display(self, obj):
        color = 'green' if obj.goods_status == 1 else 'red'
        status_text = '上架' if obj.goods_status == 1 else '下架'
        return format_html('<span style="color: {};">{}</span>', color, status_text)
    status_display.short_description = '状态'
    
    def cover_image_preview(self, obj):
        """优先显示文件上传的图片，其次显示URL图片"""
        if obj.goods_cover_img_file:
            return format_html('<img src="{}" height="50" title="文件上传" />', obj.goods_cover_img_file.url)
        elif obj.goods_cover_img:
            return format_html('<img src="{}" height="50" title="URL地址" />', obj.goods_cover_img)
        else:
            return format_html('<span style="color: red;">无图片</span>')
    cover_image_preview.short_description = '封面预览'
    
    def image_type_display(self, obj):
        """显示当前使用的图片类型"""
        if obj.goods_cover_img_file:
            return format_html('<span style="color: green;">文件上传</span>')
        elif obj.goods_cover_img:
            return format_html('<span style="color: blue;">URL地址</span>')
        else:
            return format_html('<span style="color: red;">未设置</span>')
    image_type_display.short_description = '图片类型'
    
    def get_form(self, request, obj=None, **kwargs):
        """自定义表单，为URL字段设置默认值"""
        form = super().get_form(request, obj, **kwargs)
        
        # 如果没有设置URL，可以设置默认值
        if obj and not obj.goods_cover_img:
            form.base_fields['goods_cover_img'].initial = ''
        
        return form
    
    # 批量操作
    def enable_goods(self, request, queryset):
        queryset.update(goods_status=1)
    enable_goods.short_description = "上架所选商品"
    
    def disable_goods(self, request, queryset):
        queryset.update(goods_status=0)
    disable_goods.short_description = "下架所选商品"
    
    def set_flash_sale(self, request, queryset):
        """批量设置秒杀商品"""
        from django.utils import timezone
        current_time = timezone.now()
        
        count = 0
        for goods in queryset:
            # 如果秒杀信息不完整，则自动设置默认值
            if not goods.flash_sale_price:
                goods.flash_sale_price = round(float(goods.goods_price) * 0.8, 2)  # 8折
            if goods.flash_sale_stock <= 0:
                goods.flash_sale_stock = max(10, int(goods.goods_stock * 0.3))  # 30%库存，最少10件
            if not goods.flash_sale_start_time:
                goods.flash_sale_start_time = current_time  # 立即开始
            if not goods.flash_sale_end_time:
                goods.flash_sale_end_time = current_time + timezone.timedelta(hours=24)  # 24小时后结束
            
            goods.is_flash_sale = True
            goods.save()
            count += 1
            
        self.message_user(request, f'成功设置 {count} 个商品为秒杀商品，已自动填充秒杀信息')
    set_flash_sale.short_description = "设置秒杀商品（自动填充信息）"
    
    def remove_flash_sale(self, request, queryset):
        """批量取消秒杀商品"""
        count = queryset.update(is_flash_sale=False, flash_sale_price=None, 
                              flash_sale_stock=0, flash_sale_start_time=None, 
                              flash_sale_end_time=None)
        self.message_user(request, f'成功取消 {count} 个商品的秒杀状态')
    remove_flash_sale.short_description = "取消秒杀商品"



@admin.register(GoodsCarousel)
class GoodsCarouselAdmin(admin.ModelAdmin):
    """商品轮播图Admin配置"""
    list_display = ('image_preview', 'goods_link', 'alt_text', 'sort_order', 'is_active', 'create_time')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('is_active', 'create_time')
    search_fields = ('goods__goods_name', 'alt_text')
    raw_id_fields = ('goods',)
    ordering = ('goods', 'sort_order', 'create_time')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" />', obj.image.url)
        return '-'
    image_preview.short_description = '图片预览'
    
    def goods_link(self, obj):
        return format_html('<a href="/admin/goods/goods/{}/change/">{}</a>', 
                         obj.goods.goods_id, obj.goods.goods_name)
    goods_link.short_description = '所属商品'


@admin.register(GoodsParam)
class GoodsParamAdmin(admin.ModelAdmin):
    """商品参数Admin配置"""
    list_display = ('param_name', 'param_value', 'goods_link', 'create_time')
    list_filter = ('create_time',)
    search_fields = ('param_name', 'param_value', 'goods__goods_name')
    raw_id_fields = ('goods',)
    
    def goods_link(self, obj):
        return format_html('<a href="/admin/goods/goods/{}/change/">{}</a>', 
                         obj.goods.goods_id, obj.goods.goods_name)
    goods_link.short_description = '所属商品'
  


