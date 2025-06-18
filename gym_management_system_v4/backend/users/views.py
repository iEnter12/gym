from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from bookings.models import Booking
from reviews.models import Review

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats_view(request):
    """获取用户统计信息"""
    try:
        # 获取用户信息
        user = request.user
        
        # 获取预约统计
        booking_stats = {
            'total': Booking.objects.filter(account_id=user.account_id).count(),
            'active': Booking.objects.filter(
                account_id=user.account_id,
                status='active'
            ).count(),
            'completed': Booking.objects.filter(
                account_id=user.account_id,
                status='completed'
            ).count(),
            'cancelled': Booking.objects.filter(
                account_id=user.account_id,
                status='cancelled'
            ).count()
        }
        
        # 获取评论统计
        review_stats = {
            'total': Review.objects.filter(account_id=user.account_id).count(),
            'average_rating': Review.objects.filter(
                account_id=user.account_id
            ).aggregate(Avg('rating'))['rating__avg'] or 0
        }
        
        return Response({
            'success': True,
            'data': {
                'booking_stats': booking_stats,
                'review_stats': review_stats
            }
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取用户统计失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)