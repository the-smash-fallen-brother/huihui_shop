from rest_framework import serializers
from .models import MainMenu, SubMenu

class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenu
        fields = ['sub_menu_id', 'sub_menu_name', 'sub_menu_url', 'sub_menu_icon', 'sort_order']

class MainMenuSerializer(serializers.ModelSerializer):
    sub_menus = SubMenuSerializer(many=True, read_only=True)
    
    class Meta:
        model = MainMenu
        fields = ['menu_id', 'menu_name', 'menu_url', 'menu_icon', 'sort_order', 'sub_menus']
