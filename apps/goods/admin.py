from django.contrib import admin
from django.utils.html import format_html
from .models import GoodsCategory, Goods, GoodsSpec, GoodsParam
# 定义内连类
class GoodsSpecInline:
    """商品类型内联编辑"""
    model=GoodsSpec
    pass
class GoodsParamInline:
    """商品参数内联编辑"""
    model=GoodsParam
    pass



class GoodsCategoryInline(admin.TabularInline):
    """二级分类内联编辑"""
    model = GoodsCategory
    fk_name = 'parent'  # 指定父关联字段
    extra = 1
    fields = ('category_name', 'category_level', 'category_icon', 'sort_order', 'status')
    ordering = ('sort_order',)

class GoodsParamInline(admin.TabularInline):
    """商品参数内联编辑"""
    model = GoodsParam
    extra = 1
    fields = ('param_name', 'param_value')
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
    list_display = ('goods_id','goods_name', 'category', 'goods_price', 'goods_stock', 
                   'goods_sales', 'status_display', 'cover_preview', 'create_time')
    list_editable = ('goods_price', 'goods_stock')  # 现在这些字段都在 list_display 中
    
    # 保留原有的自定义显示方法（但只用于非可编辑字段）
    def price_display(self, obj):
        return f'¥{obj.goods_price}'
    price_display.short_description = '价格展示'  # 改个不同的名称避免混淆
    
    def stock_sales_display(self, obj):
        return f'库存: {obj.goods_stock} | 销量: {obj.goods_sales}'
    stock_sales_display.short_description = '库存/销量'
    def status_display(self, obj):
        return '上架' if obj.goods_status == 1 else '下架'
    status_display.short_description = '状态'
    
    def cover_preview(self, obj):
        if obj.goods_cover_img:
            return format_html('<img src="{}" height="50" />', obj.goods_cover_img)
        return '-'
    cover_preview.short_description = '封面图'
    
    # 批量操作
    def enable_goods(self, request, queryset):
        queryset.update(goods_status=1)
    enable_goods.short_description = "上架所选商品"
    
    def disable_goods(self, request, queryset):
        queryset.update(goods_status=0)
    disable_goods.short_description = "下架所选商品"



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
  


