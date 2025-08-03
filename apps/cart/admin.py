from django.contrib import admin
from django.utils.html import format_html
from .models import ShoppingCart
@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """购物车管理配置（完整优化版）"""
    list_display = (
        'cart_id',
        'user_info',
        'goods_info',
        'goods_num',
        'selected',
        'selected_icon',  # 新增图标显示列
        'price_info',
        'total_price',
        'create_short_time'
    )
    list_editable = ('goods_num', 'selected')
    list_filter = ('selected', 'create_time')
    search_fields = (
        'user__username',
        'user__mobile',
        'goods__goods_name',
        'goods__category__category_name'
    )
    raw_id_fields = ('user', 'goods')
    list_per_page = 20
    actions = ['select_all_items', 'unselect_all_items']
    readonly_fields = ('total_price', 'create_time', 'update_time', 'selected_icon')
    date_hierarchy = 'create_time'

    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'goods', 'goods_num', 'selected')
        }),
        ('价格信息', {
            'fields': ('price_info', 'total_price'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('create_time', 'update_time'),
            'classes': ('collapse',)
        }),
    )

    # 自定义字段显示方法
    def user_info(self, obj):
        return f"{obj.user.username} (ID:{obj.user.user_id})"
    user_info.short_description = '用户'

    def goods_info(self, obj):
        return format_html(
            '{}<br><small>分类: {}</small>',
            obj.goods.goods_name,
            obj.goods.category.category_name
        )
    goods_info.short_description = '商品信息'

    def price_info(self, obj):
        return format_html(
            '单价: ¥{}<br>市场价: <s>¥{}</s>',
            obj.goods.goods_price,
            obj.goods.market_price
        )
    price_info.short_description = '价格'

    def total_price(self, obj):
        return f"¥{obj.goods.goods_price * obj.goods_num:.2f}"
    total_price.short_description = '小计'

    def selected_icon(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if obj.selected else 'red',
            '✓' if obj.selected else '✗'
        )
    selected_icon.short_description = '选中状态'

    def create_short_time(self, obj):
        return obj.create_time.strftime('%Y-%m-%d %H:%M')
    create_short_time.short_description = '添加时间'

    # 批量操作
    def select_all_items(self, request, queryset):
        updated = queryset.update(selected=True)
        self.message_user(request, f"已选中{updated}个商品")
    select_all_items.short_description = "批量选中"

    def unselect_all_items(self, request, queryset):
        updated = queryset.update(selected=False)
        self.message_user(request, f"已取消选中{updated}个商品")
    unselect_all_items.short_description = "批量取消选中"