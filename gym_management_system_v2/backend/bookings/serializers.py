from rest_framework import serializers
from .models import Booking
from accounts.models import Account
from facilities.models import Facility
from datetime import datetime, time


class BookingSerializer(serializers.ModelSerializer):
    """预约记录序列化器"""
    
    account_username = serializers.CharField(source='account.username', read_only=True)
    account_real_name = serializers.CharField(source='account.real_name', read_only=True)
    facility_name = serializers.CharField(source='facility.facility_name', read_only=True)
    facility_location = serializers.CharField(source='facility.location', read_only=True)
    facility_price = serializers.DecimalField(source='facility.price', max_digits=10, decimal_places=2, read_only=True)
    status_display = serializers.CharField(read_only=True)
    duration_hours = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'account', 'account_username', 'account_real_name',
            'facility', 'facility_name', 'facility_location', 'facility_price',
            'booking_date', 'start_time', 'end_time', 'person_count',
            'total_amount', 'status', 'status_display', 'remark',
            'is_member_used', 'cancel_reason', 'cancel_time',
            'duration_hours', 'create_time', 'update_time'
        ]
        read_only_fields = [
            'booking_id', 'total_amount', 'cancel_time', 'create_time', 'update_time'
        ]
    
    def validate(self, attrs):
        """验证预约数据"""
        booking_date = attrs.get('booking_date')
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        facility = attrs.get('facility')
        
        # 验证日期不能是过去
        if booking_date and booking_date < datetime.now().date():
            raise serializers.ValidationError("不能预约过去的日期")
        
        # 验证时间段
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError("结束时间必须晚于开始时间")
        
        # 验证场馆状态
        if facility and facility.status != 1:
            raise serializers.ValidationError("该场馆当前不可预约")
        
        # 验证时间冲突（创建时）
        if not self.instance:  # 创建新预约
            conflict_booking = Booking.objects.filter(
                facility=facility,
                booking_date=booking_date,
                status__in=[0, 1],  # 未开始或进行中
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()
            
            if conflict_booking:
                raise serializers.ValidationError("该时间段已被预约")
        
        return attrs
    
    def create(self, validated_data):
        """创建预约"""
        # 计算总金额
        facility = validated_data['facility']
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']
        
        # 计算时长（小时）
        start_datetime = datetime.combine(validated_data['booking_date'], start_time)
        end_datetime = datetime.combine(validated_data['booking_date'], end_time)
        duration = (end_datetime - start_datetime).total_seconds() / 3600
        
        # 计算总金额
        total_amount = float(facility.price) * duration
        validated_data['total_amount'] = total_amount
        
        return super().create(validated_data)


class CreateBookingSerializer(serializers.Serializer):
    """创建预约序列化器"""
    
    facility_id = serializers.IntegerField()
    booking_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    participants = serializers.IntegerField(default=1, min_value=1)
    purpose = serializers.CharField(max_length=500, required=False, allow_blank=True)
    contact_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    contact_name = serializers.CharField(max_length=50, required=False, allow_blank=True)
    remark = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_facility_id(self, value):
        """验证场馆ID"""
        try:
            facility = Facility.objects.get(facility_id=value)
            if facility.status != 1:
                raise serializers.ValidationError("该场馆当前不可预约")
            return value
        except Facility.DoesNotExist:
            raise serializers.ValidationError("场馆不存在")
    
    def validate(self, attrs):
        """验证预约数据"""
        booking_date = attrs['booking_date']
        start_time = attrs['start_time']
        end_time = attrs['end_time']
        facility_id = attrs['facility_id']
        participants = attrs['participants']
        
        # 验证日期
        if booking_date < datetime.now().date():
            raise serializers.ValidationError("不能预约过去的日期")
        
        # 验证时间
        if start_time >= end_time:
            raise serializers.ValidationError("结束时间必须晚于开始时间")
        
        # 获取场馆信息
        try:
            facility = Facility.objects.get(facility_id=facility_id)
        except Facility.DoesNotExist:
            raise serializers.ValidationError("场馆不存在")
        
        # 验证人数
        if participants > facility.capacity:
            raise serializers.ValidationError(f"预约人数不能超过场馆容量({facility.capacity}人)")
        
        # 验证预约时长
        duration = (datetime.combine(booking_date, end_time) - 
                   datetime.combine(booking_date, start_time)).total_seconds() / 3600
        
        if duration < facility.min_booking_duration:
            raise serializers.ValidationError(f"预约时长不能少于{facility.min_booking_duration}小时")
        
        if duration > facility.max_booking_duration:
            raise serializers.ValidationError(f"预约时长不能超过{facility.max_booking_duration}小时")
        
        # 验证时间冲突
        conflict_booking = Booking.objects.filter(
            facility_id=facility_id,
            booking_date=booking_date,
            status__in=[0, 1],
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()
        
        if conflict_booking:
            raise serializers.ValidationError("该时间段已被预约")
        
        return attrs


class BookingListSerializer(serializers.ModelSerializer):
    """预约列表序列化器（简化版）"""
    
    facility_name = serializers.CharField(source='facility.facility_name', read_only=True)
    facility_image = serializers.CharField(source='facility.image_url', read_only=True)
    status_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'facility_name', 'facility_image', 'booking_date',
            'start_time', 'end_time', 'person_count', 'total_amount',
            'status', 'status_display', 'create_time'
        ]


class CancelBookingSerializer(serializers.Serializer):
    """取消预约序列化器"""
    
    cancel_reason = serializers.CharField(max_length=255, required=False, allow_blank=True)

