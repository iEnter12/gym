from django.db import models


class Notice(models.Model):
    """公告信息模型"""
    
    NOTICE_TYPE_CHOICES = [
        (1, '系统公告'),
        (2, '营业时间'),
        (3, '活动通知'),
        (4, '维护通知'),
    ]
    
    PRIORITY_CHOICES = [
        (1, '普通'),
        (2, '重要'),
        (3, '紧急'),
    ]
    
    notice_id = models.AutoField(primary_key=True, verbose_name='公告ID')
    title = models.CharField(max_length=200, verbose_name='公告标题')
    content = models.TextField(verbose_name='公告内容')
    notice_type = models.IntegerField(choices=NOTICE_TYPE_CHOICES, default=1, verbose_name='公告类型')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1, verbose_name='优先级')
    start_time = models.DateTimeField(verbose_name='开始显示时间')
    end_time = models.DateTimeField(blank=True, null=True, verbose_name='结束显示时间')
    is_published = models.BooleanField(default=True, verbose_name='发布状态')
    is_top = models.BooleanField(default=False, verbose_name='是否置顶')
    view_count = models.IntegerField(default=0, verbose_name='查看次数')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'notices'
        verbose_name = '公告信息'
        verbose_name_plural = '公告信息'
        indexes = [
            models.Index(fields=['notice_type']),
            models.Index(fields=['is_published']),
            models.Index(fields=['start_time']),
            models.Index(fields=['end_time']),
            models.Index(fields=['is_top']),
            models.Index(fields=['priority']),
        ]
        ordering = ['-is_top', '-priority', '-create_time']
    
    def __str__(self):
        return self.title
    
    @property
    def notice_type_display(self):
        """公告类型显示"""
        return dict(self.NOTICE_TYPE_CHOICES).get(self.notice_type, '未知')
    
    @property
    def priority_display(self):
        """优先级显示"""
        return dict(self.PRIORITY_CHOICES).get(self.priority, '未知')
    
    def is_active(self):
        """是否在有效期内"""
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_published:
            return False
        
        if self.start_time > now:
            return False
        
        if self.end_time and self.end_time < now:
            return False
        
        return True
    
    def increment_view_count(self):
        """增加查看次数"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

