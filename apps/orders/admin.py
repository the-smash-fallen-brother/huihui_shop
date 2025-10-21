from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count, F
from .models import Order, OrderItem

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """订单项单独管理菜单"""
    list_display = [
        'item_id', 'get_order_no', 'get_order_status', 'goods', 
        'goods_name', 'goods_price', 'goods_num', 
        'goods_total_price', 'create_time'
    ]
    list_display_links = ['item_id', 'get_order_no']
    list_filter = ['create_time', 'order__order_status', 'order__payment_type']
    search_fields = [
        'order__order_no', 
        'goods_name', 
        'goods__goods_name',
        'order__receiver_name',
        'order__receiver_mobile'
    ]
    readonly_fields = [
        'item_id', 'order', 'goods', 'goods_name', 
        'goods_cover_img_display', 'goods_price', 'goods_num', 
        'goods_total_price', 'create_time'
    ]
    
    def get_order_no(self, obj):
        return f"{obj.order.order_no}"
    get_order_no.short_description = '订单编号'
    
    def get_order_status(self, obj):
        return obj.order.get_order_status_display()
    get_order_status.short_description = '订单状态'
    
    def goods_cover_img_display(self, obj):
        if obj.goods_cover_img:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', 
                             obj.goods_cover_img)
        return "无图片"
    goods_cover_img_display.short_description = '商品图片'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

class OrderItemInline(admin.TabularInline):
    """订单项内联显示-在订单详情中展示所有商品"""
    model = OrderItem
    extra = 0
    readonly_fields = [
        'goods', 'goods_name', 'goods_cover_img_display', 
        'goods_price', 'goods_num', 'goods_total_price'
    ]
    can_delete = False
    
    def goods_cover_img_display(self, obj):
        if obj.goods_cover_img:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', 
                             obj.goods_cover_img)
        return "无图片"
    goods_cover_img_display.short_description = '商品图片'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """订单主管理菜单"""
    list_display = [
        'order_no', 'get_order_status_display', 'user', 
        'total_amount', 'payment_amount', 'get_payment_type_display',
        'get_items_count', 'receiver_name', 'create_time', 
        'payment_time'
    ]
    list_display_links = ['order_no']
    list_filter = ['order_status', 'payment_type', 'create_time', 'payment_time']
    search_fields = [
        'order_no', 'user__username', 
        'receiver_name', 'receiver_mobile'
    ]
    readonly_fields = [
        'order_id', 'order_no', 'user', 'total_amount', 
        'payment_amount', 'shipping_fee', 'payment_type', 
        'order_status', 'payment_time', 'shipping_time', 
        'completion_time', 'receiver_name', 'receiver_mobile', 
        'receiver_address', 'remark', 'create_time', 'update_time',
        'get_items_count', 'get_items_total'
    ]
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('基本信息', {
            'fields': (
                'order_id', 'order_no', 'user', 
                'create_time', 'update_time'
            )
        }),
        ('金额信息', {
            'fields': (
                'total_amount', 'payment_amount', 'shipping_fee',
                'get_items_count', 'get_items_total'
            )
        }),
        ('状态信息', {
            'fields': (
                'order_status', 'payment_type',
                'payment_time', 'shipping_time', 'completion_time'
            )
        }),
        ('收货信息', {
            'fields': (
                'receiver_name', 'receiver_mobile', 
                'receiver_address', 'remark'
            )
        }),
    )
    
    def get_payment_type_display(self, obj):
        return obj.get_payment_type_display() if obj.payment_type else '未支付'
    get_payment_type_display.short_description = '支付方式'
    
    def get_items_count(self, obj):
        """显示订单中包含的商品种类数量"""
        return obj.items.count()
    get_items_count.short_description = '商品种类数'
    
    def get_items_total(self, obj):
        """显示订单中包含的商品总数量"""
        total = obj.items.aggregate(total=Sum('goods_num'))['total']
        return total or 0
    get_items_total.short_description = '商品总数量'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False