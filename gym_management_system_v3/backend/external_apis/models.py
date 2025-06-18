from django.db import models


class WeatherData(models.Model):
    """天气数据模型（缓存用）"""
    
    city = models.CharField(max_length=50, verbose_name='城市名称')
    temperature = models.IntegerField(verbose_name='温度')
    weather = models.CharField(max_length=50, verbose_name='天气状况')
    icon = models.CharField(max_length=50, verbose_name='天气图标')
    humidity = models.IntegerField(verbose_name='湿度')
    wind_speed = models.IntegerField(verbose_name='风速')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'weather_data'
        verbose_name = '天气数据'
        verbose_name_plural = '天气数据'
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['update_time']),
        ]
    
    def __str__(self):
        return f"{self.city} - {self.weather} {self.temperature}°C"


class ChatHistory(models.Model):
    """AI聊天历史模型"""
    
    chat_id = models.AutoField(primary_key=True, verbose_name='聊天ID')
    session_id = models.CharField(max_length=100, verbose_name='会话ID')
    user_message = models.TextField(verbose_name='用户消息')
    ai_response = models.TextField(verbose_name='AI回复')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'chat_history'
        verbose_name = 'AI聊天历史'
        verbose_name_plural = 'AI聊天历史'
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['create_time']),
        ]
        ordering = ['-create_time']
    
    def __str__(self):
        return f"会话 {self.session_id} - {self.create_time.strftime('%Y-%m-%d %H:%M')}"

