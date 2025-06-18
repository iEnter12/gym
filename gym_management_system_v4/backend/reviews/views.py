from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db import models, transaction
from .models import Review
from .serializers import (
    ReviewSerializer, CreateReviewSerializer,
    ReviewListSerializer, ReplyReviewSerializer
)
from accounts.models import Account
from facilities.models import Facility
from bookings.models import Booking


class ReviewListView(generics.ListAPIView):
    """评价列表"""
    
    serializer_class = ReviewListSerializer
    permission_classes = [permissions.AllowAny]  # 公开访问
    
    def get_queryset(self):
        """获取评价列表"""
        queryset = Review.objects.select_related('account', 'facility', 'booking').filter(status=1)
        
        # 筛选条件
        facility_id = self.request.query_params.get('facility_id')
        rating = self.request.query_params.get('rating')
        
        if facility_id:
            queryset = queryset.filter(facility_id=facility_id)
        
        if rating:
            queryset = queryset.filter(rating=rating)
        
        return queryset.order_by('-create_time')


class UserReviewListView(generics.ListAPIView):
    """用户评价列表"""
    
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """获取用户评价列表"""
        user = self.request.user
        
        if user.is_admin:
            # 管理员可以查看所有评价
            queryset = Review.objects.select_related('account', 'facility', 'booking').all()
        else:
            # 普通用户只能查看自己的评价
            queryset = Review.objects.select_related('facility', 'booking').filter(account_id=user.account_id)
        
        return queryset.order_by('-create_time')


class ReviewDetailView(generics.RetrieveAPIView):
    """评价详情"""
    
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'review_id'
    
    def get_queryset(self):
        """获取评价查询集"""
        return Review.objects.select_related('account', 'facility', 'booking').filter(status=1)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_review_view(request):
    """创建评价"""
    print(f"接收到的评价请求数据: {request.data}")
    print(f"当前用户: {request.user.account_id if hasattr(request.user, 'account_id') else 'Unknown'}")
    print(f"请求方法: {request.method}")
    print(f"请求头: {request.headers}")
    
    serializer = CreateReviewSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        print(f"评价数据验证通过: {serializer.validated_data}")
        try:
            with transaction.atomic():
                # 获取预约信息
                booking = Booking.objects.get(booking_id=serializer.validated_data['booking_id'])
                print(f"获取到预约信息: {booking}")
                account = Account.objects.get(account_id=request.user.account_id)
                print(f"获取到用户信息: {account}")
                
                # 创建评价
                review = Review.objects.create(
                    account=account,
                    facility=booking.facility,
                    booking=booking,
                    rating=serializer.validated_data['rating'],
                    content=serializer.validated_data.get('content', ''),
                    status=1  # 已发布
                )
                print(f"创建评价成功: {review}")
                
                # 设置图片
                images = serializer.validated_data.get('images', [])
                if images:
                    review.set_images(images)
                    review.save()
                    print(f"设置评价图片成功: {images}")
                
                response_data = {
                    'success': True,
                    'message': '评价提交成功',
                    'data': ReviewSerializer(review).data
                }
                print(f"返回响应数据: {response_data}")
                return Response(response_data)
                
        except (Booking.DoesNotExist, Account.DoesNotExist) as e:
            print(f"数据不存在错误: {str(e)}")
            return Response({
                'success': False,
                'message': '数据不存在'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"评价提交失败: {str(e)}")
            return Response({
                'success': False,
                'message': f'评价提交失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    print(f"评价数据验证失败: {serializer.errors}")
    return Response({
        'success': False,
        'message': '评价提交失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reply_review_view(request, review_id):
    """回复评价（管理员）"""
    if not request.user.is_admin:
        return Response({
            'success': False,
            'message': '权限不足'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        review = Review.objects.get(review_id=review_id)
        
        serializer = ReplyReviewSerializer(data=request.data)
        if serializer.is_valid():
            review.add_reply(serializer.validated_data['reply_content'])
            
            return Response({
                'success': True,
                'message': '回复成功',
                'data': ReviewSerializer(review).data
            })
        
        return Response({
            'success': False,
            'message': '回复失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Review.DoesNotExist:
        return Response({
            'success': False,
            'message': '评价不存在'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_review_view(request, review_id):
    """删除评价"""
    try:
        user = request.user
        
        if user.is_admin:
            review = Review.objects.get(review_id=review_id)
        else:
            review = Review.objects.get(review_id=review_id, account_id=user.account_id)
        
        # 软删除：设置状态为已删除
        review.status = 2
        review.save()
        
        return Response({
            'success': True,
            'message': '评价删除成功'
        })
        
    except Review.DoesNotExist:
        return Response({
            'success': False,
            'message': '评价不存在'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def facility_reviews_view(request, facility_id):
    """获取场馆评价"""
    try:
        facility = Facility.objects.get(facility_id=facility_id)
        
        reviews = Review.objects.select_related('account').filter(
            facility=facility,
            status=1
        ).order_by('-create_time')
        
        # 分页
        page_size = int(request.query_params.get('page_size', 10))
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        
        total = reviews.count()
        reviews_data = ReviewSerializer(reviews[start:end], many=True).data
        
        # 计算评分统计
        rating_stats = {}
        for i in range(1, 6):
            rating_stats[str(i)] = reviews.filter(rating=i).count()
        
        avg_rating = reviews.aggregate(
            avg=models.Avg('rating')
        )['avg'] or 0
        
        return Response({
            'success': True,
            'data': {
                'reviews': reviews_data,
                'total': total,
                'page': page,
                'page_size': page_size,
                'has_next': end < total,
                'statistics': {
                    'total_reviews': total,
                    'average_rating': round(float(avg_rating), 1),
                    'rating_distribution': rating_stats
                }
            }
        })
        
    except Facility.DoesNotExist:
        return Response({
            'success': False,
            'message': '场馆不存在'
        }, status=status.HTTP_404_NOT_FOUND)

