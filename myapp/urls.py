from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# import admin_tools.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin/', include(admin_tools.urls)),  # 替代默认 admin 路由
    # 用户账户模块
    path('auth/', include('apps.accounts.urls')),  # 所有账户相关路由统一前缀
    
    # 其他模块
    path('goods/', include('apps.goods.urls')),
    path('cart/', include('apps.cart.urls')),
    path('orders/', include('apps.orders.urls')),
    path('payment/', include('apps.payment.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('menus/', include('apps.menu.urls')),
]

# 开发环境下提供媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)