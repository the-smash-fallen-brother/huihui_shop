from django.contrib import admin
from .models import MainMenu, SubMenu

class SubMenuInline(admin.TabularInline):
    """
    子菜单内联编辑（在主菜单编辑页直接编辑子菜单）
    """
    model = SubMenu
    extra = 1  # 默认显示1个空表单
    fields = ('sub_menu_name', 'sub_menu_type', 'sub_menu_url', 'sub_menu_icon', 'sort_order', 'status')
    ordering = ('sort_order',)  # 按排序值排序

@admin.register(MainMenu)
class MainMenuAdmin(admin.ModelAdmin):
    """
    主菜单Admin配置
    """
    list_display = ('menu_name', 'menu_url', 'menu_icon', 'sub_menus_count', 'sort_order', 'status', 'create_time')
    list_editable = ('sort_order', 'status')  # 可直接在列表页编辑的字段
    list_filter = ('status', 'create_time')  # 右侧过滤器
    search_fields = ('menu_name', 'menu_url')  # 搜索字段
    ordering = ('sort_order', '-create_time')  # 默认排序
    inlines = [SubMenuInline]  # 内联子菜单
    
    # 自定义字段：显示关联子菜单数量
    def sub_menus_count(self, obj):
        return obj.sub_menus.count()
    sub_menus_count.short_description = '子菜单数'

    # 自定义动作
    actions = ['enable_menus', 'disable_menus']
    
    def enable_menus(self, request, queryset):
        queryset.update(status=True)
    enable_menus.short_description = "启用所选菜单"
    
    def disable_menus(self, request, queryset):
        queryset.update(status=False)
    disable_menus.short_description = "禁用所选菜单"

@admin.register(SubMenu)
class SubMenuAdmin(admin.ModelAdmin):
    """
    子菜单Admin配置
    """
    list_display = ('sub_menu_name', 'menu', 'sub_menu_type_display', 'sub_menu_url', 'sort_order', 'status', 'create_time')
    list_editable = ('sort_order', 'status')
    list_filter = ('menu', 'sub_menu_type', 'status', 'create_time')
    search_fields = ('sub_menu_name', 'sub_menu_url', 'menu__menu_name')
    raw_id_fields = ('menu',)  # 对于外键使用弹出窗口选择
    ordering = ('menu__sort_order', 'sort_order')
    
    # 显示带中文的子菜单类型
    def sub_menu_type_display(self, obj):
        return obj.get_sub_menu_type_display()
    sub_menu_type_display.short_description = '菜单类型'
    
    # 批量操作
    actions = ['set_as_normal_menu', 'set_as_function_menu']
    
    def set_as_normal_menu(self, request, queryset):
        queryset.update(sub_menu_type=1)
    set_as_normal_menu.short_description = "设为普通菜单"
    
    def set_as_function_menu(self, request, queryset):
        queryset.update(sub_menu_type=2)
    set_as_function_menu.short_description = "设为功能菜单"