from rest_framework import serializers
from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    """公告信息序列化器"""
    
    notice_type_display = serializers.CharField(read_only=True)
    priority_display = serializers.CharField(read_only=True)
    is_active = serializers.SerializerMethodField()
    
    class Meta:
        model = Notice
        fields = [
            'notice_id', 'title', 'content', 'notice_type', 'notice_type_display',
            'priority', 'priority_display', 'start_time', 'end_time',
            'is_published', 'is_top', 'view_count', 'is_active',
            'create_time', 'update_time'
        ]
        read_only_fields = ['notice_id', 'view_count', 'create_time', 'update_time']
    
    def get_is_active(self, obj):
        """获取是否在有效期内"""
        return obj.is_active()


class NoticeListSerializer(serializers.ModelSerializer):
    """公告列表序列化器（简化版）"""
    
    notice_type_display = serializers.CharField(read_only=True)
    priority_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = Notice
        fields = [
            'notice_id', 'title', 'notice_type', 'notice_type_display',
            'priority', 'priority_display', 'start_time', 'end_time',
            'is_published', 'is_top', 'view_count', 'create_time'
        ]


class CreateNoticeSerializer(serializers.ModelSerializer):
    """创建公告序列化器"""
    
    class Meta:
        model = Notice
        fields = [
            'title', 'content', 'notice_type', 'priority',
            'start_time', 'end_time', 'is_published', 'is_top'
        ]
    
    def validate(self, attrs):
        """验证公告数据"""
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        
        if end_time and start_time and end_time <= start_time:
            raise serializers.ValidationError("结束时间必须晚于开始时间")
        
        return attrs

