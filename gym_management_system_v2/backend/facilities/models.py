from django.db import models


class FacilityType(models.Model):
    """场馆类型模型"""
    
    type_id = models.AutoField(primary_key=True, verbose_name='类型ID')
    type_name = models.CharField(max_length=50, unique=True, verbose_name='类型名称')
    icon = models.CharField(max_length=255, blank=True, null=True, verbose_name='类型图标')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='类型描述')
    sort_order = models.IntegerField(default=0, verbose_name='排序顺序')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'facility_types'
        verbose_name = '场馆类型'
        verbose_name_plural = '场馆类型'
        indexes = [
            models.Index(fields=['sort_order']),
            models.Index(fields=['is_active']),
        ]
        ordering = ['sort_order', 'type_id']
    
    def __str__(self):
        return self.type_name


class Facility(models.Model):
    """场馆信息模型"""
    
    STATUS_CHOICES = [
        (1, '可用'),
        (2, '维护中'),
        (3, '已关闭'),
    ]
    
    facility_id = models.AutoField(primary_key=True, verbose_name='场馆ID')
    type = models.ForeignKey(FacilityType, on_delete=models.CASCADE, verbose_name='场馆类型')
    facility_name = models.CharField(max_length=100, unique=True, verbose_name='场馆名称')
    location = models.CharField(max_length=255, verbose_name='场馆位置')
    capacity = models.IntegerField(verbose_name='容纳人数')
    area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='面积（平方米）')
    image_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='场馆图片URL')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价（元/小时）')
    description = models.TextField(blank=True, null=True, verbose_name='场馆描述')
    opening_hours = models.CharField(max_length=100, default='06:00-22:00', verbose_name='营业时间')
    advance_booking_days = models.IntegerField(default=7, verbose_name='可提前预约天数')
    min_booking_duration = models.IntegerField(default=1, verbose_name='最小预约时长（小时）')
    max_booking_duration = models.IntegerField(default=4, verbose_name='最大预约时长（小时）')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='场馆状态')
    sort_order = models.IntegerField(default=0, verbose_name='排序顺序')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'facilities'
        verbose_name = '场馆信息'
        verbose_name_plural = '场馆信息'
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['status']),
            models.Index(fields=['sort_order']),
            models.Index(fields=['price']),
        ]
        ordering = ['sort_order', 'facility_id']
    
    def __str__(self):
        return f"{self.facility_name} ({self.type.type_name})"
    
    @property
    def is_available(self):
        """是否可用"""
        return self.status == 1
    
    @property
    def status_display(self):
        """状态显示"""
        return dict(self.STATUS_CHOICES).get(self.status, '未知')

