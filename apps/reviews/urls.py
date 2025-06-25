
from django.urls import path
from .views import (
    CommentListView,
    UserCommentListView,
    CommentCreateView
)

urlpatterns = [
    path('goods/<int:goods_id>/', CommentListView.as_view(), name='comment-list'),
    path('user/', UserCommentListView.as_view(), name='user-comment-list'),
    path('', CommentCreateView.as_view(), name='comment-create'),
]