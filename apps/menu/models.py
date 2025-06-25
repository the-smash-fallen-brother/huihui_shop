from django.db import models

class MainMenu(models.Model):
    """
    主菜单表
    """
    menu_id = models.AutoField(primary_key=True, verbose_name='菜单ID')
    menu_name = models.CharField(max_length=50, verbose_name='菜单名称')
    menu_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='菜单URL')
    menu_icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='菜单图标')
    sort_order = models.IntegerField(default=0, verbose_name='排序值')
    status = models.BooleanField(default=True, verbose_name='状态(0-禁用 1-启用)')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'main_menu'
        verbose_name = '主菜单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.menu_name


class SubMenu(models.Model):
    """
    子菜单表
    """
    SUB_MENU_TYPE_CHOICES = (
        (1, '普通菜单'),
        (2, '功能菜单')
    )
    
    sub_menu_id = models.AutoField(primary_key=True, verbose_name='子菜单ID')
    menu = models.ForeignKey(MainMenu, on_delete=models.CASCADE, related_name='sub_menus', verbose_name='主菜单')
    sub_menu_name = models.CharField(max_length=50, verbose_name='子菜单名称')
    sub_menu_type = models.SmallIntegerField(choices=SUB_MENU_TYPE_CHOICES, default=1, verbose_name='子菜单类型')
    sub_menu_url = models.CharField(max_length=255, verbose_name='子菜单URL')
    sub_menu_icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='子菜单图标')
    sort_order = models.IntegerField(default=0, verbose_name='排序值')
    status = models.BooleanField(default=True, verbose_name='状态(0-禁用 1-启用)')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'sub_menu'
        verbose_name = '子菜单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sub_menu_name
