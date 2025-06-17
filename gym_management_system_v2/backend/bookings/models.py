from django.db import models
from accounts.models import Account
from facilities.models import Facility


class Booking(models.Model):
    """预约记录模型"""
    
    STATUS_CHOICES = [
        (0, '未开始'),
        (1, '待确认'),
        (2, '进行中'),
        (3, '已完成'),
        (4, '已取消'),
        (5, '已过期'),
    ]
    
    booking_id = models.AutoField(primary_key=True, verbose_name='预约ID')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='用户')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, verbose_name='场馆')
    booking_date = models.DateField(verbose_name='预约日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    person_count = models.IntegerField(default=1, verbose_name='预约人数')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='预约状态')
    purpose = models.CharField(max_length=500, blank=True, null=True, verbose_name='预约目的')
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系电话')
    contact_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='联系人')
    remark = models.CharField(max_length=500, blank=True, null=True, verbose_name='备注信息')
    is_member_used = models.BooleanField(default=False, verbose_name='是否使用会员权益（已停用）')
    cancel_reason = models.CharField(max_length=255, blank=True, null=True, verbose_name='取消原因')
    cancel_time = models.DateTimeField(blank=True, null=True, verbose_name='取消时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'bookings'
        verbose_name = '预约记录'
        verbose_name_plural = '预约记录'
        indexes = [
            models.Index(fields=['account']),
            models.Index(fields=['facility']),
            models.Index(fields=['booking_date']),
            models.Index(fields=['status']),
            models.Index(fields=['facility', 'booking_date', 'start_time', 'end_time']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['facility', 'booking_date', 'start_time', 'end_time'],
                name='unique_facility_datetime'
            )
        ]
        ordering = ['-create_time']
    
    def __str__(self):
        return f"{self.account.username} - {self.facility.facility_name} ({self.booking_date} {self.start_time}-{self.end_time})"
    
    @property
    def status_display(self):
        """状态显示"""
        return dict(self.STATUS_CHOICES).get(self.status, '未知')
    
    @property
    def duration_hours(self):
        """预约时长（小时）"""
        from datetime import datetime, timedelta
        start_datetime = datetime.combine(self.booking_date, self.start_time)
        end_datetime = datetime.combine(self.booking_date, self.end_time)
        duration = end_datetime - start_datetime
        return duration.total_seconds() / 3600
    
    def can_cancel(self):
        """是否可以取消"""
        return self.status in [0, 1]  # 未开始或进行中
    
    def can_review(self):
        """是否可以评价"""
        return self.status == 2  # 已完成

