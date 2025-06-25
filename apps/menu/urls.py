from django.urls import path
from .views import MainMenuView, SubMenuView

urlpatterns = [
    path('main/', MainMenuView.as_view(), name='main-menu'),
    path('sub/', SubMenuView.as_view(), name='sub-menu'),
]
