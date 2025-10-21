from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_protect
from .models import ShoppingCart

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """购物车管理配置（修复版）"""
    list_display = (
        'cart_id',
        'user_info',
        'goods_info',
        'goods_num',
        # 'selected',
        # 'selected_icon',
        'price_info',
        'total_price',
        'create_short_time',
        # 'edit_actions'  # 添加编辑操作列
    )
    list_filter = ('selected', 'create_time')
    search_fields = (
        'user__username',
        'user__mobile',
        'goods__goods_name',
        'goods__category__category_name'
    )
    raw_id_fields = ('user', 'goods')
    list_per_page = 20
    # actions = ['select_all_items', 'unselect_all_items']
    readonly_fields = ()  # 清空只读字段，因为都是自动的
    date_hierarchy = 'create_time'

    # 添加自定义URL
    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path('edit-item/<int:item_id>/', self.admin_site.admin_view(self.edit_item_view), name='shoppingcart_edit_item'),
    #         path('update-item/', self.admin_site.admin_view(self.update_item_view), name='shoppingcart_update_item'),
    #     ]
    #     return custom_urls + urls

    # 简化字段集，只保留基本信息
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'goods', 'goods_num', 'selected')
        }),
    )

    # 自定义字段显示方法
    def user_info(self, obj):
        if obj.user:
            return f"{obj.user.username} (ID:{obj.user.user_id})"
        return "无用户"
    user_info.short_description = '用户'

    def goods_info(self, obj):
        if obj.goods:
            return format_html(
                '{}<br><small>分类: {}</small>',
                obj.goods.goods_name,
                obj.goods.category.category_name if obj.goods.category else '无分类'
            )
        return "无商品"
    goods_info.short_description = '商品信息'

    def price_info(self, obj):
        if obj.goods:
            return format_html(
                '单价: ¥{}<br>市场价: <s>¥{}</s>',
                obj.goods.goods_price,
                obj.goods.market_price
            )
        return "无价格信息"
    price_info.short_description = '价格'

    def total_price(self, obj):
        if obj.goods:
            return f"¥{obj.goods.goods_price * obj.goods_num:.2f}"
        return "¥0.00"
    total_price.short_description = '小计'

    def selected_icon(self, obj):
        return format_html(
            '<span style="color: {}; font-size: 16px;">{}</span>',
            'green' if obj.selected else 'red',
            '✓' if obj.selected else '✗'
        )
    selected_icon.short_description = '选中'

    def create_short_time(self, obj):
        return obj.create_time.strftime('%Y-%m-%d %H:%M')
    create_short_time.short_description = '添加时间'

    # 编辑操作按钮
    def edit_actions(self, obj):
        return format_html(
            '''
            <button class="button edit-btn" data-id="{}" 
                    style="background-color: #417690; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">
                编辑
            </button>
            ''',
            obj.cart_id
        )
    edit_actions.short_description = '操作'
    edit_actions.allow_tags = True

    # 批量操作
    def select_all_items(self, request, queryset):
        updated = queryset.update(selected=True)
        self.message_user(request, f"已选中{updated}个商品")
    select_all_items.short_description = "批量选中"

    def unselect_all_items(self, request, queryset):
        updated = queryset.update(selected=False)
        self.message_user(request, f"已取消选中{updated}个商品")
    unselect_all_items.short_description = "批量取消选中"

   
    