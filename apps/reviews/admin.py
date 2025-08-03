from django.contrib import admin
from .models import Comment, CommentImage

class CommentImageInline(admin.TabularInline):
    """
    Inline admin interface for CommentImage model
    """
    model = CommentImage
    extra = 0  # Number of empty forms to display
    fields = ('image_url', 'sort_order', 'create_time')
    readonly_fields = ('create_time',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface for Comment model
    """
    list_display = ('comment_id', 'user', 'goods', 'rating', 'comment_time', 'has_reply')
    list_filter = ('rating', 'comment_time', 'goods')
    search_fields = ('content', 'user__username', 'goods__name')
    readonly_fields = ('comment_time', 'update_time')
    date_hierarchy = 'comment_time'
    inlines = [CommentImageInline]
    
    fieldsets = (
        (None, {
            'fields': ('user', 'goods', 'order', 'rating')
        }),
        ('评论内容', {
            'fields': ('content',)
        }),
        ('商家回复', {
            'fields': ('reply_content', 'reply_time'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('comment_time', 'update_time'),
            'classes': ('collapse',)
        }),
    )
    
    def has_reply(self, obj):
        return bool(obj.reply_content)
    has_reply.boolean = True
    has_reply.short_description = '已回复'

@admin.register(CommentImage)
class CommentImageAdmin(admin.ModelAdmin):
    """
    Admin interface for CommentImage model
    """
    list_display = ('image_id', 'comment', 'image_url_short', 'sort_order', 'create_time')
    list_filter = ('comment__goods', 'create_time')
    search_fields = ('comment__content', 'image_url')
    readonly_fields = ('create_time',)
    
    def image_url_short(self, obj):
        return obj.image_url[:50] + '...' if len(obj.image_url) > 50 else obj.image_url
    image_url_short.short_description = '图片URL'