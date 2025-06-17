from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db import models, transaction
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Booking
from .serializers import (
    BookingSerializer, CreateBookingSerializer,
    BookingListSerializer, CancelBookingSerializer
)
# 已删除订单模块导入
from accounts.models import Account
from facilities.models import Facility


class BookingListView(generics.ListAPIView):
    """预约列表"""
    
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """获取预约列表"""
        user = self.request.user
        
        if user.is_admin:
            # 管理员可以查看所有预约
            queryset = Booking.objects.select_related('account', 'facility').all()
        else:
            # 普通用户只能查看自己的预约
            queryset = Booking.objects.select_related('facility').filter(account_id=user.account_id)
        
        # 筛选条件
        status_filter = self.request.query_params.get('status')
        date_filter = self.request.query_params.get('date')
        facility_id = self.request.query_params.get('facility_id')
        
        if status_filter is not None:
            queryset = queryset.filter(status=status_filter)
        
        if date_filter:
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                queryset = queryset.filter(booking_date=filter_date)
            except ValueError:
                pass
        
        if facility_id:
            queryset = queryset.filter(facility_id=facility_id)
        
        return queryset.order_by('-create_time')


class BookingDetailView(generics.RetrieveAPIView):
    """预约详情"""
    
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'booking_id'
    
    def get_queryset(self):
        """获取预约查询集"""
        user = self.request.user
        
        if user.is_admin:
            return Booking.objects.select_related('account', 'facility').all()
        else:
            return Booking.objects.select_related('facility').filter(account_id=user.account_id)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_booking_view(request):
    """创建预约"""
    print("接收到的请求数据:", request.data)  # 添加日志
    
    serializer = CreateBookingSerializer(data=request.data)
    if serializer.is_valid():
        try:
            with transaction.atomic():
                # 获取用户账户
                try:
                    account = Account.objects.get(account_id=request.user.account_id)
                except Account.DoesNotExist:
                    return Response({
                        'success': False,
                        'message': '用户不存在'
                    }, status=status.HTTP_404_NOT_FOUND)

                # 获取 facility 实例
                facility_id = serializer.validated_data['facility_id']
                try:
                    facility = Facility.objects.get(pk=facility_id)
                except Facility.DoesNotExist:
                    return Response({
                        'success': False,
                        'message': '场馆不存在'
                    }, status=status.HTTP_404_NOT_FOUND)

                # 获取时间段信息
                start_time = serializer.validated_data['start_time']
                end_time = serializer.validated_data['end_time']
                booking_date = serializer.validated_data['booking_date']
                participants = serializer.validated_data['participants']
                purpose = serializer.validated_data.get('purpose', '')
                contact_phone = serializer.validated_data.get('contact_phone', '')
                contact_name = serializer.validated_data.get('contact_name', '')
                remark = serializer.validated_data.get('remark', '')

                # 计算总金额
                start_datetime = datetime.combine(booking_date, start_time)
                end_datetime = datetime.combine(booking_date, end_time)
                duration = (end_datetime - start_datetime).total_seconds() / 3600
                total_amount = float(facility.price) * duration

                # 创建预约
                booking = Booking.objects.create(
                    account=account,
                    facility=facility,
                    booking_date=booking_date,
                    start_time=start_time,
                    end_time=end_time,
                    person_count=participants,
                    total_amount=total_amount,
                    purpose=purpose,
                    contact_phone=contact_phone,
                    contact_name=contact_name,
                    remark=remark,
                    status=1  # 待确认
                )

                return Response({
                    'success': True,
                    'message': '预约成功',
                    'data': {
                        'booking_id': booking.booking_id
                    }
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            import traceback
            print("错误详情:", str(e))  # 添加日志
            print("错误堆栈:", traceback.format_exc())  # 添加日志
            return Response({
                'success': False,
                'message': f'预约创建失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    print("验证错误:", serializer.errors)  # 添加日志
    return Response({
        'success': False,
        'message': '预约创建失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def cancel_booking_view(request, booking_id):
    """取消预约"""
    try:
        user = request.user
        
        if user.is_admin:
            booking = Booking.objects.get(booking_id=booking_id)
        else:
            booking = Booking.objects.get(booking_id=booking_id, account_id=user.account_id)
        
        if not booking.can_cancel():
            return Response({
                'success': False,
                'message': '该预约无法取消'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CancelBookingSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                # 更新预约状态
                booking.status = 3  # 已取消
                booking.cancel_reason = serializer.validated_data.get('cancel_reason', '')
                booking.cancel_time = timezone.now()
                booking.save()
                
                # 已删除订单退款逻辑
                
                return Response({
                    'success': True,
                    'message': '预约取消成功'
                })
        
        return Response({
            'success': False,
            'message': '取消失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Booking.DoesNotExist:
        return Response({
            'success': False,
            'message': '预约不存在'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def confirm_booking_view(request, booking_id):
    """确认预约（管理员）"""
    if not request.user.is_admin:
        return Response({
            'success': False,
            'message': '权限不足'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        booking = Booking.objects.get(booking_id=booking_id)
        
        if booking.status != 0:  # 只能确认未开始的预约
            return Response({
                'success': False,
                'message': '该预约无法确认'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = 1  # 进行中
        booking.save()
        
        return Response({
            'success': True,
            'message': '预约确认成功'
        })
        
    except Booking.DoesNotExist:
        return Response({
            'success': False,
            'message': '预约不存在'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def complete_booking_view(request, booking_id):
    """完成预约"""
    try:
        user = request.user
        
        if user.is_admin:
            booking = Booking.objects.get(booking_id=booking_id)
        else:
            booking = Booking.objects.get(booking_id=booking_id, account_id=user.account_id)
        
        if booking.status != 1:  # 只能完成进行中的预约
            return Response({
                'success': False,
                'message': '该预约无法完成'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = 2  # 已完成
        booking.save()
        
        return Response({
            'success': True,
            'message': '预约完成'
        })
        
    except Booking.DoesNotExist:
        return Response({
            'success': False,
            'message': '预约不存在'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_statistics_view(request):
    """仪表盘统计数据（管理员）"""
    if not request.user.is_admin:
        return Response({
            'success': False,
            'message': '权限不足'
        }, status=status.HTTP_403_FORBIDDEN)
    
    today = timezone.now().date()
    
    # 今日预约数
    today_bookings = Booking.objects.filter(booking_date=today).count()
    
    # 本周预约数
    week_start = today - timedelta(days=today.weekday())
    week_bookings = Booking.objects.filter(
        booking_date__gte=week_start,
        booking_date__lte=today
    ).count()
    
    # 本月预约数
    month_bookings = Booking.objects.filter(
        booking_date__year=today.year,
        booking_date__month=today.month
    ).count()
    
    # 总用户数
    total_users = Account.objects.filter(user_type=1).count()
    
    # 活跃用户数（本月有预约的用户）
    active_users = Account.objects.filter(
        booking__booking_date__year=today.year,
        booking__booking_date__month=today.month
    ).distinct().count()
    
    # 场馆数量
    total_facilities = Facility.objects.count()
    available_facilities = Facility.objects.filter(status=1).count()
    
    return Response({
        'success': True,
        'data': {
            'bookings': {
                'today': today_bookings,
                'week': week_bookings,
                'month': month_bookings
            },
            'users': {
                'total': total_users,
                'active': active_users
            },
            'facilities': {
                'total': total_facilities,
                'available': available_facilities
            }
        }
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats_view(request):
    """获取用户统计数据"""
    user = request.user
    
    # 获取用户的所有预约
    user_bookings = Booking.objects.filter(account_id=user.account_id)
    
    # 统计各种状态的预约数量
    total_bookings = user_bookings.count()
    completed_bookings = user_bookings.filter(status='completed').count()
    cancelled_bookings = user_bookings.filter(status='cancelled').count()
    pending_bookings = user_bookings.filter(status='pending').count()
    
    return Response({
        'success': True,
        'data': {
            'total': total_bookings,
            'completed': completed_bookings,
            'cancelled': cancelled_bookings,
            'pending': pending_bookings
        }
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_bookings_view(request):
    """获取用户预约列表"""
    try:
        # 获取用户的预约记录
        bookings = Booking.objects.filter(
            account_id=request.user.account_id
        ).select_related('facility').order_by('-create_time')
        
        # 序列化数据
        serializer = BookingListSerializer(bookings, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取预约列表失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

