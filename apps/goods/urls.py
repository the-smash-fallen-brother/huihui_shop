
from django.urls import path
from .views import (
    GoodsCategoryListView,
    GoodsListView,
    GoodsDetailView,
    GoodsHotView,
    GoodsNewView,
    GoodsSearchView,
    GoodsSpecView,
    GoodsParamView
)

urlpatterns = [
    path('categories/', GoodsCategoryListView.as_view(), name='goods-category-list'),
    path('list/', GoodsListView.as_view(), name='goods-list'),
    path('detail/<int:goods_id>/', GoodsDetailView.as_view(), name='goods-detail'),
    path('hot/', GoodsHotView.as_view(), name='goods-hot'),
    path('new/', GoodsNewView.as_view(), name='goods-new'),
    path('search/', GoodsSearchView.as_view(), name='goods-search'),
    path('<int:goods_id>/specs/', GoodsSpecView.as_view(), name='goods-specs'),
    path('<int:goods_id>/params/', GoodsParamView.as_view(), name='goods-params'),
]