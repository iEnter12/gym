from rest_framework import serializers
from .models import Review
from accounts.models import Account
from facilities.models import Facility
from bookings.models import Booking
import json


class ReviewSerializer(serializers.ModelSerializer):
    """评价记录序列化器"""
    
    account_username = serializers.CharField(source='account.username', read_only=True)
    account_real_name = serializers.CharField(source='account.real_name', read_only=True)
    facility_name = serializers.CharField(source='facility.facility_name', read_only=True)
    booking_date = serializers.DateField(source='booking.booking_date', read_only=True)
    status_display = serializers.CharField(read_only=True)
    image_list = serializers.ListField(read_only=True)
    has_reply = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'review_id', 'account', 'account_username', 'account_real_name',
            'facility', 'facility_name', 'booking', 'booking_date',
            'rating', 'content', 'images', 'image_list', 'reply_content',
            'reply_time', 'status', 'status_display', 'has_reply',
            'create_time', 'update_time'
        ]
        read_only_fields = [
            'review_id', 'reply_time', 'create_time', 'update_time'
        ]


class CreateReviewSerializer(serializers.Serializer):
    """创建评价序列化器"""
    
    booking_id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    content = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    images = serializers.ListField(
        child=serializers.URLField(),
        required=False,
        allow_empty=True,
        max_length=5  # 最多5张图片
    )
    
    def validate_booking_id(self, value):
        """验证预约ID"""
        try:
            booking = Booking.objects.get(booking_id=value)
            
            # 检查预约是否已完成
            if booking.status != 2:
                raise serializers.ValidationError("只能对已完成的预约进行评价")
            
            # 检查是否已经评价过
            if Review.objects.filter(booking=booking).exists():
                raise serializers.ValidationError("该预约已经评价过了")
            
            # 检查是否是当前用户的预约
            request = self.context.get('request')
            if request and booking.account_id != request.user.account_id:
                raise serializers.ValidationError("只能评价自己的预约")
            
            return value
        except Booking.DoesNotExist:
            raise serializers.ValidationError("预约不存在")


class ReviewListSerializer(serializers.ModelSerializer):
    """评价列表序列化器（简化版）"""
    
    account_username = serializers.CharField(source='account.username', read_only=True)
    facility_name = serializers.CharField(source='facility.facility_name', read_only=True)
    status_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'review_id', 'account_username', 'facility_name', 'rating',
            'content', 'status', 'status_display', 'create_time'
        ]


class ReplyReviewSerializer(serializers.Serializer):
    """回复评价序列化器"""
    
    reply_content = serializers.CharField(max_length=500)

