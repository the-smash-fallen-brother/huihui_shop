from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import MainMenu, SubMenu
from .serializers import MainMenuSerializer, SubMenuSerializer

class MainMenuView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request):
        menus = MainMenu.objects.filter(status=True).prefetch_related(
            'sub_menus'
        ).order_by('sort_order')
        
        for menu in menus:
            menu.sub_menus = menu.sub_menus.filter(status=True).order_by('sort_order')
            
        serializer = MainMenuSerializer(menus, many=True)
        return Response({
            'code': 200,
            'message': '成功',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class SubMenuView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request):
        sub_menus = SubMenu.objects.filter(
            status=True
        ).select_related('menu').order_by('sort_order')
        
        serializer = SubMenuSerializer(sub_menus, many=True)
        return Response({
            'code': 200,
            'message': '成功',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
