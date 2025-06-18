from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    """用户账户模型"""
    
    USER_TYPE_CHOICES = [
        (1, '普通用户'),
        (2, '管理员'),
    ]
    
    STATUS_CHOICES = [
        (1, '正常'),
        (2, '禁用'),
    ]
    
    account_id = models.AutoField(primary_key=True, verbose_name='账户ID')
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    real_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='真实姓名')
    id_card = models.CharField(max_length=20, blank=True, null=True, verbose_name='身份证号')
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name='手机号')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='邮箱')
    avatar = models.CharField(max_length=255, blank=True, null=True, verbose_name='头像URL')
    register_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    last_login_time = models.DateTimeField(blank=True, null=True, verbose_name='最后登录时间')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='账户状态')
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=1, verbose_name='用户类型')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'accounts'
        verbose_name = '用户账户'
        verbose_name_plural = '用户账户'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['phone']),
            models.Index(fields=['user_type']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.real_name or '未设置姓名'})"
    
    @property
    def is_admin(self):
        """是否为管理员"""
        return self.user_type == 2
    
    @property
    def is_active_user(self):
        """是否为活跃用户"""
        return self.status == 1


class SystemConfig(models.Model):
    """系统配置模型"""
    
    CONFIG_TYPE_CHOICES = [
        ('string', '字符串'),
        ('number', '数字'),
        ('boolean', '布尔值'),
        ('json', 'JSON'),
    ]
    
    config_id = models.AutoField(primary_key=True, verbose_name='配置ID')
    config_key = models.CharField(max_length=100, unique=True, verbose_name='配置键名')
    config_value = models.TextField(blank=True, null=True, verbose_name='配置值')
    config_type = models.CharField(max_length=20, choices=CONFIG_TYPE_CHOICES, default='string', verbose_name='配置类型')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='配置描述')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'system_configs'
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置'
        indexes = [
            models.Index(fields=['config_key']),
            models.Index(fields=['is_public']),
        ]
    
    def __str__(self):
        return f"{self.config_key}: {self.config_value}"


class OperationLog(models.Model):
    """操作日志模型"""
    
    log_id = models.AutoField(primary_key=True, verbose_name='日志ID')
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='操作用户')
    operation_type = models.CharField(max_length=50, verbose_name='操作类型')
    operation_desc = models.CharField(max_length=255, blank=True, null=True, verbose_name='操作描述')
    request_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='请求URL')
    request_method = models.CharField(max_length=10, blank=True, null=True, verbose_name='请求方法')
    request_params = models.TextField(blank=True, null=True, verbose_name='请求参数')
    response_status = models.IntegerField(blank=True, null=True, verbose_name='响应状态码')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')
    user_agent = models.CharField(max_length=500, blank=True, null=True, verbose_name='用户代理')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'operation_logs'
        verbose_name = '操作日志'
        verbose_name_plural = '操作日志'
        indexes = [
            models.Index(fields=['account']),
            models.Index(fields=['operation_type']),
            models.Index(fields=['create_time']),
        ]
    
    def __str__(self):
        return f"{self.operation_type} - {self.account.username if self.account else '匿名'}"

