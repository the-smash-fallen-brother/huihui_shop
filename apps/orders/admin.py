from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """订单项内联编辑"""
    model = OrderItem
    extra = 0
    readonly_fields = (
        'goods_name', 
        'goods_cover_img_preview',
        'goods_price',
        'goods_total_price'
    )
    fields = (
        'goods', 
        'goods_name', 
        'goods_cover_img_preview',
        'goods_price',
        'goods_num',
        'goods_total_price'
    )
    
    def goods_cover_img_preview(self, obj):
        if obj.goods_cover_img:
            return format_html('<img src="{}" height="50" />', obj.goods_cover_img)
        return "无图片"
    goods_cover_img_preview.short_description = '商品图片'

class OrderAdminForm(forms.ModelForm):
    """订单管理表单"""
    class Meta:
        model = Order
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 在添加新订单时，设置一些字段的初始值
        if not self.instance.pk:  # 新订单
            self.fields['order_status'].initial = 1  # 默认待付款
            self.fields['payment_type'].initial = 1  # 默认支付方式

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """订单管理配置"""
    form = OrderAdminForm
    
    list_display = (
        'order_no',
        'user_info',
        'payment_amount_display',
        'order_status_display',
        'payment_type_display',
        'receiver_info',
        'create_short_time',
        'action_buttons'
    )
    list_filter = (
        'order_status',
        'payment_type',
        'create_time'
    )
    search_fields = (
        'order_no',
        'user__username',
        'user__mobile',
        'receiver_name',
        'receiver_mobile'
    )
    raw_id_fields = ('user',)
    list_per_page = 20
    inlines = [OrderItemInline]
    actions = [
        'mark_as_paid',
        'mark_as_shipped',
        'mark_as_completed',
        'export_orders'
    ]
    date_hierarchy = 'create_time'
    
    fieldsets = (
        ('订单信息', {
            'fields': (
                # 'order_no',
                'user',
                ('total_amount', 'payment_amount', 'shipping_fee'),
                ('order_status', 'payment_type')
            )
        }),
        ('支付信息', {
            'fields': (
                'payment_time',
                'shipping_time',
                'completion_time'
            ),
            'classes': ('collapse',)
        }),
        ('收货信息', {
            'fields': (
                'receiver_name',
                'receiver_mobile', 
                'receiver_address',
                'remark'
            )
        }),
        ('时间信息', {
            'fields': ('create_time', 'update_time'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """动态设置只读字段"""
        if obj:  # 编辑现有订单
            return (
                'order_no',
                'total_amount',
                'payment_amount',
                'shipping_fee',
                'create_time',
                'update_time'
            )
        else:  # 添加新订单
            return ('create_time', 'update_time')

    def save_model(self, request, obj, form, change):
        """保存模型时自动生成订单编号"""
        if not change:  # 新订单
            # 自动生成订单编号
            import datetime
            import random
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            random_str = str(random.randint(1000, 9999))
            obj.order_no = f'ORD{timestamp}{random_str}'
            
            # 设置默认金额值（如果未填写）
            if not obj.total_amount:
                obj.total_amount = 0
            if not obj.payment_amount:
                obj.payment_amount = obj.total_amount
            if obj.shipping_fee is None:
                obj.shipping_fee = 0
        
        super().save_model(request, obj, form, change)

    # 自定义字段显示方法
    def user_info(self, obj):
        if obj.user:
            # 使用 user_id 而不是 id
            return f"{obj.user.username}(ID:{obj.user.user_id})"
        return "无用户"
    user_info.short_description = '用户'

    def payment_amount_display(self, obj):
        return f"¥{obj.payment_amount:.2f}" if obj.payment_amount else "¥0.00"
    payment_amount_display.short_description = '实付金额'

    def order_status_display(self, obj):
        status_map = {
            0: ('已取消', 'gray'),
            1: ('待付款', 'red'),
            2: ('待发货', 'orange'),
            3: ('待收货', 'blue'),
            4: ('已完成', 'green')
        }
        text, color = status_map.get(obj.order_status, ('未知', 'black'))
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, text
        )
    order_status_display.short_description = '订单状态'

    def payment_type_display(self, obj):
        return dict(Order.PAYMENT_TYPE_CHOICES).get(obj.payment_type, '未支付')
    payment_type_display.short_description = '支付方式'

    def receiver_info(self, obj):
        if obj.receiver_name and obj.receiver_mobile:
            return format_html(
                '{} {}<br>{}',
                obj.receiver_name,
                obj.receiver_mobile,
                obj.receiver_address[:20] + '...' if obj.receiver_address and len(obj.receiver_address) > 20 else obj.receiver_address
            )
        return "未设置"
    receiver_info.short_description = '收货信息'

    def create_short_time(self, obj):
        return obj.create_time.strftime('%Y-%m-%d %H:%M') if obj.create_time else ""
    create_short_time.short_description = '下单时间'

    def action_buttons(self, obj):
        buttons = []
        if obj.order_status == 1:  # 待付款
            buttons.append('<a class="button" href="mark_as_paid/">标记为已付款</a>')
        if obj.order_status == 2:  # 待发货
            buttons.append('<a class="button" href="mark_as_shipped/">标记为已发货</a>')
        if obj.order_status == 3:  # 待收货
            buttons.append('<a class="button" href="mark_as_completed/">标记为已完成</a>')
        return format_html(' '.join(buttons)) if buttons else "无操作"
    action_buttons.short_description = '操作'

    # 批量操作方法
    def mark_as_paid(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(order_status=1).update(
            order_status=2,
            payment_time=timezone.now()
        )
        self.message_user(request, f"{updated}个订单已标记为已付款")
    mark_as_paid.short_description = "标记为已付款"

    def mark_as_shipped(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(order_status=2).update(
            order_status=3,
            shipping_time=timezone.now()
        )
        self.message_user(request, f"{updated}个订单已标记为已发货")
    mark_as_shipped.short_description = "标记为已发货"

    def mark_as_completed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(order_status=3).update(
            order_status=4,
            completion_time=timezone.now()
        )
        self.message_user(request, f"{updated}个订单已标记为已完成")
    mark_as_completed.short_description = "标记为已完成"

    def export_orders(self, request, queryset):
        """导出订单"""
        from django.http import HttpResponse
        import csv
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['订单编号', '用户', '金额', '状态', '下单时间'])
        
        for order in queryset:
            writer.writerow([
                order.order_no,
                order.user.username if order.user else '',
                float(order.payment_amount) if order.payment_amount else 0,
                order.get_order_status_display(),
                order.create_time.strftime('%Y-%m-%d %H:%M') if order.create_time else ''
            ])
        return response
    export_orders.short_description = "导出选中订单"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """订单项管理配置"""
    list_display = (
        'item_id',
        'order_link',
        'goods_link',
        'goods_cover_img_preview',
        'goods_price_display',
        'goods_num',
        'goods_total_price_display',
        'create_short_time'
    )
    list_filter = ('create_time', 'order__order_no')
    search_fields = (
        'order__order_no',
        'goods__goods_name',
        'goods_name'
    )
    raw_id_fields = ('order', 'goods')
    readonly_fields = ('goods_cover_img_preview',)
    list_per_page = 20
    
    def order_link(self, obj):
        if obj.order:
            # 使用 order_id 而不是 id
            return format_html(
                '<a href="/admin/orders/order/{}/change/">{}</a>',
                obj.order.order_id,  # 修改这里
                obj.order.order_no
            )
        return "无订单"
    order_link.short_description = '订单编号'
    
    def goods_link(self, obj):
        if obj.goods:
            # 使用 goods_id 而不是 id
            return format_html(
                '<a href="/admin/goods/goods/{}/change/">{}</a>',
                obj.goods.goods_id,  # 修改这里
                obj.goods_name or obj.goods.goods_name
            )
        return format_html('<span>{}</span>', obj.goods_name or "无商品")
    goods_link.short_description = '商品名称'
    
    def goods_cover_img_preview(self, obj):
        if obj.goods_cover_img:
            return format_html(
                '<img src="{}" height="50" />', 
                obj.goods_cover_img
            )
        return "无图片"
    goods_cover_img_preview.short_description = '商品图片'
    
    def goods_price_display(self, obj):
        return f"¥{obj.goods_price:.2f}" if obj.goods_price else "¥0.00"
    goods_price_display.short_description = '单价'
    
    def goods_total_price_display(self, obj):
        return f"¥{obj.goods_total_price:.2f}" if obj.goods_total_price else "¥0.00"
    goods_total_price_display.short_description = '总价'
    
    def create_short_time(self, obj):
        return obj.create_time.strftime('%Y-%m-%d %H:%M') if obj.create_time else ""
    create_short_time.short_description = '创建时间'

    # 可选：隐藏 OrderItem 的独立入口，避免混淆
    def get_model_perms(self, request):
        """在Admin首页隐藏OrderItem模型"""
        return {}