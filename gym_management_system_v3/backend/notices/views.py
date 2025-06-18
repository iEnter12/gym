from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db import models
from django.utils import timezone
from .models import Notice
from .serializers import (
    NoticeSerializer, NoticeListSerializer, CreateNoticeSerializer
)


class NoticeListView(generics.ListCreateAPIView):
    """公告列表"""
    
    permission_classes = [permissions.AllowAny]  # 公开访问
    
    def get_serializer_class(self):
        """根据请求方法选择序列化器"""
        if self.request.method == 'POST':
            return CreateNoticeSerializer
        return NoticeListSerializer
    
    def get_queryset(self):
        """获取公告列表"""
        now = timezone.now()
        
        # 默认只显示已发布且在有效期内的公告
        queryset = Notice.objects.filter(
            is_published=True,
            start_time__lte=now
        ).filter(
            models.Q(end_time__isnull=True) | models.Q(end_time__gte=now)
        )
        
        # 管理员可以查看所有公告
        if self.request.user.is_authenticated and self.request.user.is_admin:
            queryset = Notice.objects.all()
        
        # 筛选条件
        notice_type = self.request.query_params.get('notice_type')
        priority = self.request.query_params.get('priority')
        
        if notice_type:
            queryset = queryset.filter(notice_type=notice_type)
        
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset.order_by('-is_top', '-priority', '-create_time')
    
    def get_permissions(self):
        """根据请求方法设置权限"""
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        """创建公告（管理员）"""
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("权限不足")
        serializer.save()


class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """公告详情"""
    
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    lookup_field = 'notice_id'
    
    def get_permissions(self):
        """根据请求方法设置权限"""
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def retrieve(self, request, *args, **kwargs):
        """获取公告详情并增加查看次数"""
        instance = self.get_object()
        
        # 增加查看次数
        instance.increment_view_count()
        
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def perform_update(self, serializer):
        """更新公告（管理员）"""
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("权限不足")
        serializer.save()
    
    def perform_destroy(self, instance):
        """删除公告（管理员）"""
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("权限不足")
        instance.delete()
    
    def update(self, request, *args, **kwargs):
        """更新公告"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'success': True,
            'message': '公告更新成功',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        """删除公告"""
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({
            'success': True,
            'message': '公告删除成功'
        })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def active_notices_view(request):
    """获取当前有效的公告"""
    now = timezone.now()
    
    notices = Notice.objects.filter(
        is_published=True,
        start_time__lte=now
    ).filter(
        models.Q(end_time__isnull=True) | models.Q(end_time__gte=now)
    ).order_by('-is_top', '-priority', '-create_time')
    
    # 限制数量
    limit = int(request.query_params.get('limit', 10))
    notices = notices[:limit]
    
    serializer = NoticeListSerializer(notices, many=True)
    
    return Response({
        'success': True,
        'data': serializer.data
    })


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def toggle_notice_status_view(request, notice_id):
    """切换公告发布状态（管理员）"""
    if not request.user.is_admin:
        return Response({
            'success': False,
            'message': '权限不足'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        notice = Notice.objects.get(notice_id=notice_id)
        notice.is_published = not notice.is_published
        notice.save()
        
        status_text = '发布' if notice.is_published else '取消发布'
        
        return Response({
            'success': True,
            'message': f'公告{status_text}成功',
            'data': NoticeSerializer(notice).data
        })
        
    except Notice.DoesNotExist:
        return Response({
            'success': False,
            'message': '公告不存在'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def toggle_notice_top_view(request, notice_id):
    """切换公告置顶状态（管理员）"""
    if not request.user.is_admin:
        return Response({
            'success': False,
            'message': '权限不足'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        notice = Notice.objects.get(notice_id=notice_id)
        notice.is_top = not notice.is_top
        notice.save()
        
        status_text = '置顶' if notice.is_top else '取消置顶'
        
        return Response({
            'success': True,
            'message': f'公告{status_text}成功',
            'data': NoticeSerializer(notice).data
        })
        
    except Notice.DoesNotExist:
        return Response({
            'success': False,
            'message': '公告不存在'
        }, status=status.HTTP_404_NOT_FOUND)

