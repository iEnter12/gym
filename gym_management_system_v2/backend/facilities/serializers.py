from rest_framework import serializers
from .models import FacilityType, Facility


class FacilityTypeSerializer(serializers.ModelSerializer):
    """场馆类型序列化器"""
    
    class Meta:
        model = FacilityType
        fields = '__all__'
        read_only_fields = ['type_id', 'create_time']


class FacilitySerializer(serializers.ModelSerializer):
    """场馆信息序列化器"""
    
    type_name = serializers.CharField(source='type.type_name', read_only=True)
    type_icon = serializers.CharField(source='type.icon', read_only=True)
    status_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = Facility
        fields = [
            'facility_id', 'type', 'type_name', 'type_icon', 'facility_name',
            'location', 'capacity', 'area', 'image_url', 'price', 'description',
            'opening_hours', 'advance_booking_days', 'min_booking_duration',
            'max_booking_duration', 'status', 'status_display', 'sort_order',
            'create_time', 'update_time'
        ]
        read_only_fields = ['facility_id', 'create_time', 'update_time']


class FacilityListSerializer(serializers.ModelSerializer):
    """场馆列表序列化器（简化版）"""
    
    type_name = serializers.CharField(source='type.type_name', read_only=True)
    type_icon = serializers.CharField(source='type.icon', read_only=True)
    status_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = Facility
        fields = [
            'facility_id', 'type', 'type_name', 'type_icon', 'facility_name',
            'location', 'capacity', 'image_url', 'price', 'status', 'status_display'
        ]


class FacilityDetailSerializer(serializers.ModelSerializer):
    """场馆详情序列化器"""
    
    type_info = FacilityTypeSerializer(source='type', read_only=True)
    status_display = serializers.CharField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Facility
        fields = [
            'facility_id', 'type', 'type_info', 'facility_name', 'location',
            'capacity', 'area', 'image_url', 'price', 'description',
            'opening_hours', 'advance_booking_days', 'min_booking_duration',
            'max_booking_duration', 'status', 'status_display', 'is_available',
            'sort_order', 'create_time', 'update_time'
        ]

