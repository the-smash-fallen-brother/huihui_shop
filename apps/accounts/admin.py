from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserAddress

class CustomUserAdmin(UserAdmin):
    list_display = ('user_id', 'username', 'mobile', 'email', 'is_active')
    search_fields = ('username', 'mobile', 'email')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('mobile', 'email', 'gender', 'avatar_url', 'birthday')}),
        ('状态', {'fields': ('status', 'is_active', 'is_staff', 'is_superuser')}),
        ('时间', {'fields': ('last_login', 'date_joined')}),
    )

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'user', 'receiver_name', 'receiver_mobile', 'is_default')
    list_filter = ('is_default', 'province', 'city')
    raw_id_fields = ('user',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserAddress, UserAddressAdmin)