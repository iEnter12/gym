from django.db import models
from accounts.models import Account
from facilities.models import Facility
from bookings.models import Booking
import json


class Review(models.Model):
    """评价记录模型"""
    
    STATUS_CHOICES = [
        (1, '已发布'),
        (2, '已删除'),
        (3, '已隐藏'),
    ]
    
    review_id = models.AutoField(primary_key=True, verbose_name='评价ID')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='用户')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, verbose_name='场馆')
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, verbose_name='预约记录')
    rating = models.IntegerField(verbose_name='评分（1-5分）')
    content = models.CharField(max_length=1000, blank=True, null=True, verbose_name='评价内容')
    images = models.TextField(blank=True, null=True, verbose_name='评价图片URL（JSON格式）')
    reply_content = models.CharField(max_length=500, blank=True, null=True, verbose_name='管理员回复内容')
    reply_time = models.DateTimeField(blank=True, null=True, verbose_name='回复时间')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='评价状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'reviews'
        verbose_name = '评价记录'
        verbose_name_plural = '评价记录'
        indexes = [
            models.Index(fields=['account']),
            models.Index(fields=['facility']),
            models.Index(fields=['rating']),
            models.Index(fields=['status']),
        ]
        ordering = ['-create_time']
    
    def __str__(self):
        return f"{self.account.username} 对 {self.facility.facility_name} 的评价 ({self.rating}分)"
    
    @property
    def status_display(self):
        """状态显示"""
        return dict(self.STATUS_CHOICES).get(self.status, '未知')
    
    @property
    def image_list(self):
        """获取图片列表"""
        if self.images:
            try:
                return json.loads(self.images)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_images(self, image_urls):
        """设置图片列表"""
        if isinstance(image_urls, list):
            self.images = json.dumps(image_urls)
        else:
            self.images = None
    
    def add_reply(self, reply_content):
        """添加管理员回复"""
        from django.utils import timezone
        self.reply_content = reply_content
        self.reply_time = timezone.now()
        self.save()
    
    @property
    def has_reply(self):
        """是否有回复"""
        return bool(self.reply_content)

