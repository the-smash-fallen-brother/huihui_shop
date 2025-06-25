from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
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