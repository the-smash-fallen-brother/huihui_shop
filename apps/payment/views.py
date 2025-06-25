from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.payment.models import PaymentInfo
from django.utils import timezone  
from apps.payment.serializers import PaymentInfoSerializer
from apps.orders.models import Order
import time

class PaymentView(APIView):
    """
    支付接口
    GET /orders/{order_id}/payment/ - 获取支付信息
    POST /orders/{order_id}/pay/ - 模拟支付
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        """获取支付信息"""
        try:
            order = Order.objects.get(order_id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)

        if order.order_status != 1:
            return Response({'error': '只有待付款订单可以支付'}, status=status.HTTP_400_BAD_REQUEST)

        payment = PaymentInfo.objects.filter(order=order).first()
        if not payment:
            payment = PaymentInfo.objects.create(
                order=order,
                order_no=order.order_no,
                payment_type=1,  # 默认支付宝
                payment_amount=order.payment_amount,
                payment_status=0
            )

        serializer = PaymentInfoSerializer(payment)
        return Response(serializer.data)

    def post(self, request, order_id):
        """处理支付请求"""
        try:
            order = Order.objects.get(order_id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)

        if order.order_status != 1:
            return Response({'error': '只有待付款订单可以支付'}, status=status.HTTP_400_BAD_REQUEST)

        payment_type = request.data.get('payment_type', 1)
        payment = PaymentInfo.objects.create(
            order=order,
            order_no=order.order_no,
            payment_type=payment_type,
            payment_amount=order.payment_amount,
            payment_status=1,
            payment_time=timezone.now(),
            transaction_id=str(int(time.time() * 1000))  # 模拟交易号
        )
        
        # 更新订单状态
        order.order_status = 2  # 待发货
        order.payment_time = timezone.now()
        order.save()

        return Response({
            'message': '支付成功', 
            'payment_id': payment.payment_id,
            'transaction_id': payment.transaction_id
        }, status=status.HTTP_200_OK)