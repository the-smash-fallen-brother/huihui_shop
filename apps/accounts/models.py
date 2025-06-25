from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.goods.models import Goods
class User(AbstractUser):
    """
    用户模型 - 继承AbstractUser并保持原有字段
    """
    class Gender(models.IntegerChoices):
        UNKNOWN = 0, _('未知')
        MALE = 1, _('男')
        FEMALE = 2, _('女')

    # 保留原有字段
    user_id = models.AutoField(primary_key=True, verbose_name=_('用户ID'))
    mobile = models.CharField(max_length=11, unique=True, verbose_name=_('手机号'))
    gender = models.SmallIntegerField(
        choices=Gender.choices, 
        default=Gender.UNKNOWN,
        verbose_name=_('性别')
    )
    avatar_url = models.URLField(max_length=255, blank=True, null=True, verbose_name=_('头像URL'))
    birthday = models.DateField(blank=True, null=True, verbose_name=_('生日'))
    status = models.SmallIntegerField(default=1, verbose_name=_('状态(0-禁用 1-正常)'))
    last_login_time = models.DateTimeField(blank=True, null=True, verbose_name=_('最后登录时间'))
    
    # 元数据保持原样
    class Meta:
        app_label = 'accounts'
        db_table = 'user'
        verbose_name = _('用户')
        verbose_name_plural = verbose_name

    # 保持原有输出格式
    def __str__(self):
        return str({
            'user_id': self.user_id,
            'username': self.username,
            'mobile': self.mobile,
            'email': self.email
        })

class UserFavorite(models.Model):
    """
    用户收藏商品关系表
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='用户'
    )
    goods = models.ForeignKey(
        Goods,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='商品'
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        db_table = 'user_favorite'
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'goods')  # 确保用户不能重复收藏同一商品

    def __str__(self):
        return f"{self.user.username}收藏-{self.goods.goods_name}"


class UserAddress(models.Model):
    """
    用户地址模型 - 完全保持原有结构
    """
    address_id = models.AutoField(primary_key=True, verbose_name=_('地址ID'))
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name=_('用户')
    )
    receiver_name = models.CharField(max_length=50, verbose_name=_('收货人姓名'))
    receiver_mobile = models.CharField(max_length=11, verbose_name=_('收货人手机号'))
    province = models.CharField(max_length=50, verbose_name=_('省'))
    city = models.CharField(max_length=50, verbose_name=_('市'))
    district = models.CharField(max_length=50, verbose_name=_('区/县'))
    detailed_address = models.CharField(max_length=255, verbose_name=_('详细地址'))
    is_default = models.BooleanField(default=False, verbose_name=_('是否默认地址'))
    
    # 时间字段
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'))
    update_time = models.DateTimeField(auto_now=True, verbose_name=_('更新时间'))

    class Meta:
        app_label = 'accounts'
        db_table = 'user_address'
        verbose_name = _('用户地址')
        verbose_name_plural = verbose_name
        ordering = ['-is_default', '-create_time']

    def __str__(self):
        return str({
            'address_id': self.address_id,
            'user_id': self.user_id,
            'receiver_name': self.receiver_name,
            'is_default': self.is_default
        })

    def save(self, *args, **kwargs):
        """保证只有一个默认地址"""
        if self.is_default:
            UserAddress.objects.filter(
                user=self.user, 
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)