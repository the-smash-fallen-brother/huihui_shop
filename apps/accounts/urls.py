from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

app_name = 'accounts'  # 添加命名空间

urlpatterns = [
    # 认证模块
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # 用户模块
    path('info/', UserInfoView.as_view(), name='user-info'),
    path('password/', UserPasswordView.as_view(), name='user-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #更新token
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    # 地址管理
    path('addresses/', UserAddressView.as_view(), name='address-list'),
    path('addresses/<int:address_id>/', UserAddressDetailView.as_view(), name='address-detail'),
    path('addresses/default/', UserAddressView.as_view(), name='address-default'),
    
    # 收藏管理
    path('favorites/', UserFavoriteView.as_view(), name='favorite-list'),
    path('favorites/<int:goods_id>/', UserFavoriteView.as_view(), name='favorite-detail'),
    path('favorites/check/', UserFavoriteCheckView.as_view(), name='favorite-check')
]