from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone  
from apps.orders.models import Order, OrderItem
from apps.orders.serializers import OrderSerializer, OrderDetailSerializer
from apps.cart.models import ShoppingCart
from apps.goods.models import Goods

class OrderView(generics.ListCreateAPIView):
    """
    订单接口
    GET /orders/ - 获取订单列表
    POST /orders/ - 创建订单
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-create_time')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        address_id = request.data.get('address_id')
        cart_item_ids = request.data.get('cart_item_ids', [])
        remark = request.data.get('remark', '')

        # 验证地址
        try:
            address = user.addresses.get(address_id=address_id)
        except:
            return Response({'error': '地址不存在'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取选中的购物车商品
        cart_items = ShoppingCart.objects.filter(
            cart_id__in=cart_item_ids, 
            user=user, 
            selected=True
        ).select_related('goods')

        if not cart_items:
            return Response({'error': '没有选中的商品'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建订单
        order = Order.objects.create(
            user=user,
            total_amount=0,
            payment_amount=0,
            shipping_fee=0,
            order_status=1,
            receiver_name=address.receiver_name,
            receiver_mobile=address.receiver_mobile,
            receiver_address=f"{address.province}{address.city}{address.district}{address.detailed_address}",
            remark=remark
        )

        total_amount = 0
        # 创建订单项
        for cart_item in cart_items:
            goods = cart_item.goods
            if goods.goods_stock < cart_item.goods_num:
                transaction.set_rollback(True)
                return Response({'error': f'{goods.goods_name}库存不足'}, status=status.HTTP_400_BAD_REQUEST)

            item_total = goods.goods_price * cart_item.goods_num
            OrderItem.objects.create(
                order=order,
                goods=goods,
                goods_name=goods.goods_name,
                goods_cover_img=goods.goods_cover_img,
                goods_price=goods.goods_price,
                goods_num=cart_item.goods_num,
                goods_total_price=item_total
            )

            # 更新商品库存和销量
            goods.goods_stock -= cart_item.goods_num
            goods.goods_sales += cart_item.goods_num
            goods.save()

            total_amount += item_total
            cart_item.delete()

        # 更新订单金额
        order.total_amount = total_amount
        order.payment_amount = total_amount  # 这里可以加上运费和优惠计算
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveAPIView):
    """
    订单详情接口
    GET /orders/{order_id}/ - 获取订单详情
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderDetailSerializer
    lookup_field = 'order_id'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCancelView(generics.GenericAPIView):
    """
    取消订单接口
    POST /orders/{order_id}/cancel/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)

        if order.order_status != 1:
            return Response({'error': '只有待付款订单可以取消'}, status=status.HTTP_400_BAD_REQUEST)

        order.order_status = 0
        order.save()

        # 恢复库存
        order_items = order.items.all()
        for item in order_items:
            goods = item.goods
            goods.goods_stock += item.goods_num
            goods.goods_sales -= item.goods_num
            goods.save()

        return Response({'message': '订单已取消'})


class OrderConfirmView(generics.GenericAPIView):
    """
    确认收货接口
    POST /orders/{order_id}/confirm/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)

        if order.order_status != 3:
            return Response({'error': '只有待收货订单可以确认'}, status=status.HTTP_400_BAD_REQUEST)

        order.order_status = 4
        order.completion_time = timezone.now()
        order.save()
        return Response({'message': '订单已完成'})
