from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db import models
from datetime import datetime, timedelta, time
from .models import FacilityType, Facility
from .serializers import (
    FacilityTypeSerializer, FacilitySerializer,
    FacilityListSerializer, FacilityDetailSerializer
)
from bookings.models import Booking


class FacilityTypeListView(generics.ListCreateAPIView):
    """场馆类型列表"""
    
    queryset = FacilityType.objects.filter(is_active=True).order_by('sort_order', 'type_id')
    serializer_class = FacilityTypeSerializer
    permission_classes = [permissions.AllowAny]  # 公开访问
    
    def get_permissions(self):
        """根据请求方法设置权限"""
        if self.request.method == 'POST':
            # 只有管理员可以创建
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        """创建场馆类型（管理员）"""
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("权限不足")
        serializer.save()


class FacilityTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """场馆类型详情"""
    
    queryset = FacilityType.objects.all()
    serializer_class = FacilityTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'type_id'
    
    def get_permissions(self):
        """根据请求方法设置权限"""
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def perform_update(self, serializer):
        """更新场馆类型（管理员）"""
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("权限不足")
        serializer.save()
    
    def perform_destroy(self, instance):
        """删除场馆类型（管理员）"""
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("权限不足")
        # 软删除：设置为不活跃
        instance.is_active = False
        instance.save()


class FacilityListView(generics.ListCreateAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [permissions.AllowAny]  # 允许公开访问列表
    
    def get_queryset(self):
        queryset = Facility.objects.select_related('type').all()
        
        # 获取查询参数
        type_id = self.request.query_params.get('type_id')
        status = self.request.query_params.get('status')
        keyword = self.request.query_params.get('keyword')
        
        # 应用过滤条件
        if type_id:
            queryset = queryset.filter(type_id=type_id)
        if status:
            queryset = queryset.filter(status=status)
        if keyword:
            queryset = queryset.filter(
                models.Q(facility_name__icontains=keyword) |
                models.Q(location__icontains=keyword)
            )
        
        return queryset.order_by('sort_order', 'facility_id')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # 构建标准响应格式
        response_data = {
            'success': True,
            'data': serializer.data,
            'total': queryset.count(),
            'message': '获取场馆列表成功'
        }
        
        return Response(response_data)
    
    def get_permissions(self):
        """根据请求方法设置权限"""
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        """创建场馆（管理员）"""
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("权限不足")
        serializer.save()


class FacilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """场馆详情"""
    
    queryset = Facility.objects.select_related('type').all()
    serializer_class = FacilityDetailSerializer
    lookup_field = 'facility_id'
    
    def get_permissions(self):
        """根据请求方法设置权限"""
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def perform_update(self, serializer):
        """更新场馆（管理员）"""
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("权限不足")
        serializer.save()
    
    def perform_destroy(self, instance):
        """删除场馆（管理员）"""
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("权限不足")
        instance.delete()


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def facility_available_slots_view(request, facility_id):
    """获取场馆可用时间段"""
    try:
        facility = Facility.objects.get(facility_id=facility_id)
        date_str = request.query_params.get('date')
        
        if not date_str:
            return Response({
                'success': False,
                'message': '请提供日期参数'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({
                'success': False,
                'message': '日期格式错误，请使用YYYY-MM-DD格式'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查是否在可预约范围内
        today = datetime.now().date()
        max_date = today + timedelta(days=facility.advance_booking_days)
        
        if booking_date < today:
            return Response({
                'success': False,
                'message': '不能预约过去的日期'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if booking_date > max_date:
            return Response({
                'success': False,
                'message': f'最多只能提前{facility.advance_booking_days}天预约'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取已预约的时间段
        booked_slots = Booking.objects.filter(
            facility=facility,
            booking_date=booking_date,
            status__in=[0, 1]  # 未开始或进行中
        ).values_list('start_time', 'end_time')
        
        # 生成可用时间段
        available_slots = generate_available_slots(
            facility.opening_hours,
            facility.min_booking_duration,
            facility.max_booking_duration,
            booked_slots
        )
        
        return Response({
            'success': True,
            'data': {
                'facility_id': facility.facility_id,
                'facility_name': facility.facility_name,
                'date': date_str,
                'available_slots': available_slots
            }
        })
        
    except Facility.DoesNotExist:
        return Response({
            'success': False,
            'message': '场馆不存在'
        }, status=status.HTTP_404_NOT_FOUND)


def generate_available_slots(opening_hours, min_duration, max_duration, booked_slots):
    """生成可用时间段"""
    # 解析营业时间
    try:
        start_str, end_str = opening_hours.split('-')
        start_hour, start_minute = map(int, start_str.split(':'))
        end_hour, end_minute = map(int, end_str.split(':'))
        
        start_time = time(start_hour, start_minute)
        end_time = time(end_hour, end_minute)
    except:
        # 默认营业时间
        start_time = time(6, 0)
        end_time = time(22, 0)
    
    available_slots = []
    current_time = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)
    
    # 按小时生成时间段
    while current_time < end_datetime:
        slot_start = current_time.time()
        slot_end = (current_time + timedelta(hours=min_duration)).time()
        
        if slot_end <= end_time:
            # 检查是否与已预约时间冲突
            is_available = True
            for booked_start, booked_end in booked_slots:
                if (slot_start < booked_end and slot_end > booked_start):
                    is_available = False
                    break
            
            if is_available:
                available_slots.append({
                    'start_time': slot_start.strftime('%H:%M'),
                    'end_time': slot_end.strftime('%H:%M'),
                    'duration': min_duration
                })
        
        current_time += timedelta(hours=1)
    
    return available_slots

