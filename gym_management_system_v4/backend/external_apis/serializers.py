from rest_framework import serializers
from .models import WeatherData, ChatHistory


class WeatherDataSerializer(serializers.ModelSerializer):
    """天气数据序列化器"""
    
    class Meta:
        model = WeatherData
        fields = '__all__'


class ChatHistorySerializer(serializers.ModelSerializer):
    """AI聊天历史序列化器"""
    
    class Meta:
        model = ChatHistory
        fields = '__all__'
        read_only_fields = ['chat_id', 'create_time']


class ChatRequestSerializer(serializers.Serializer):
    """AI聊天请求序列化器"""
    
    message = serializers.CharField(max_length=1000)
    session_id = serializers.CharField(max_length=100, required=False)
    
    def validate_message(self, value):
        """验证消息内容"""
        if not value.strip():
            raise serializers.ValidationError("消息内容不能为空")
        return value.strip()

