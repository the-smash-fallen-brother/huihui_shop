from django.db import models
from apps.accounts.models import User
from apps.goods.models import Goods
from apps.orders.models import Order

class Comment(models.Model):
    """
    商品评论表
    """
    RATING_CHOICES = (
        (1, '1星'),
        (2, '2星'),
        (3, '3星'),
        (4, '4星'),
        (5, '5星')
    )
    
    comment_id = models.AutoField(primary_key=True, verbose_name='评论ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='用户')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='comments', verbose_name='商品')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='comments', verbose_name='订单')
    content = models.TextField(verbose_name='评论内容')
    rating = models.SmallIntegerField(choices=RATING_CHOICES, verbose_name='评分')
    reply_content = models.TextField(blank=True, null=True, verbose_name='商家回复内容')
    reply_time = models.DateTimeField(blank=True, null=True, verbose_name='商家回复时间')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        app_label = 'reviews'
        db_table = 'comment'
        verbose_name = '商品评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return {
            'comment_id': self.comment_id,
            'user_id': self.user_id,
            'goods_id': self.goods_id,
            'order_id': self.order_id,
            'rating': self.rating,
            'comment_time': self.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        }.__str__()


class CommentImage(models.Model):
    """
    评论图片表
    """
    image_id = models.AutoField(primary_key=True, verbose_name='图片ID')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='images', verbose_name='评论')
    image_url = models.ImageField(upload_to='comment_images/', verbose_name='图片')
    sort_order = models.IntegerField(default=0, verbose_name='排序值')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        app_label = 'reviews'
        db_table = 'comment_image'
        verbose_name = '评论图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return {
            'image_id': self.image_id,
            'comment_id': self.comment_id,
            'image_url': self.image_url
        }.__str__()
