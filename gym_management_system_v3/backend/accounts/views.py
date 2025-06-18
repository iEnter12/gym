from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db import models
from .models import Account, SystemConfig, OperationLog
from .serializers import (
    AccountSerializer, LoginSerializer, RegisterSerializer,
    UserProfileSerializer, ChangePasswordSerializer,
    SystemConfigSerializer, OperationLogSerializer
)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """用户登录"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        account = serializer.validated_data['account']
        
        # 更新最后登录时间
        account.last_login_time = timezone.now()
        account.save()
        
        # 获取或创建Token
        token, created = Token.objects.get_or_create(user=account)
        
        # 记录操作日志
        OperationLog.objects.create(
            account=account,
            operation_type='login',
            operation_desc='用户登录',
            request_url=request.path,
            request_method=request.method,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({
            'success': True,
            'data': {
                'token': token.key,
                'user': AccountSerializer(account).data
            }
        })
    
    return Response({
        'success': False,
        'message': '登录失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """用户注册"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        account = serializer.save()
        
        # 记录操作日志
        OperationLog.objects.create(
            account=account,
            operation_type='register',
            operation_desc='用户注册',
            request_url=request.path,
            request_method=request.method,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({
            'success': True,
            'message': '注册成功',
            'data': AccountSerializer(account).data
        })
    
    return Response({
        'success': False,
        'message': '注册失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_info_view(request):
    """获取用户信息"""
    try:
        # 直接使用request.user，因为它已经是认证后的用户对象
        return Response({
            'success': True,
            'data': UserProfileSerializer(request.user).data
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_profile_view(request):
    """更新用户资料"""
    try:
        account = Account.objects.get(account_id=request.user.account_id)
        serializer = UserProfileSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': '资料更新成功',
                'data': serializer.data
            })
        
        return Response({
            'success': False,
            'message': '资料更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except Account.DoesNotExist:
        return Response({
            'success': False,
            'message': '用户不存在'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def change_password_view(request):
    """修改密码"""
    try:
        print("开始处理密码修改请求")
        print("请求数据:", request.data)
        
        account = Account.objects.get(account_id=request.user.account_id)
        print("找到用户:", account.username)
        
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        print("序列化器创建完成")
        
        if not serializer.is_valid():
            print("序列化器验证失败:", serializer.errors)
            return Response({
                'success': False,
                'message': '密码修改失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            print("开始设置新密码")
            account.set_password(serializer.validated_data['new_password'])
            account.save()
            print("密码设置成功")
            
            # 记录操作日志
            OperationLog.objects.create(
                account=account,
                operation_type='change_password',
                operation_desc='修改密码',
                request_url=request.path,
                request_method=request.method,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            print("操作日志记录完成")
            
            return Response({
                'success': True,
                'message': '密码修改成功'
            })
        except Exception as e:
            print("设置密码时发生错误:", str(e))
        return Response({
            'success': False,
                'message': f'密码修改失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Account.DoesNotExist:
        print("用户不存在")
        return Response({
            'success': False,
            'message': '用户不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("发生未知错误:", str(e))
        return Response({
            'success': False,
            'message': f'系统错误: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def logout_view(request):
    """用户退出"""
    try:
        account = Account.objects.get(account_id=request.user.account_id)
        
        # 删除Token
        Token.objects.filter(user=account).delete()
        
        # 记录操作日志
        OperationLog.objects.create(
            account=account,
            operation_type='logout',
            operation_desc='用户退出',
            request_url=request.path,
            request_method=request.method,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({
            'success': True,
            'message': '退出成功'
        })
    except Account.DoesNotExist:
        return Response({
            'success': False,
            'message': '用户不存在'
        }, status=status.HTTP_404_NOT_FOUND)


class UserListView(generics.ListAPIView):
    """用户列表（管理员）"""
    
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # 只有管理员可以查看用户列表
        if not self.request.user.is_admin:
            return Account.objects.none()
        
        queryset = Account.objects.all()
        
        # 筛选条件
        user_type = self.request.query_params.get('user_type')
        status_filter = self.request.query_params.get('status')
        keyword = self.request.query_params.get('keyword')
        
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if keyword:
            queryset = queryset.filter(
                models.Q(username__icontains=keyword) |
                models.Q(real_name__icontains=keyword) |
                models.Q(phone__icontains=keyword)
            )
        
        return queryset.order_by('-create_time')


@api_view(['PUT'])
def update_user_status_view(request, user_id):
    """更新用户状态（管理员）"""
    if not request.user.is_admin:
        return Response({
            'success': False,
            'message': '权限不足'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        account = Account.objects.get(account_id=user_id)
        new_status = request.data.get('status')
        
        if new_status not in [1, 2]:
            return Response({
                'success': False,
                'message': '无效的状态值'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        account.status = new_status
        account.save()
        
        return Response({
            'success': True,
            'message': '状态更新成功'
        })
    except Account.DoesNotExist:
        return Response({
            'success': False,
            'message': '用户不存在'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def reset_user_password_view(request, user_id):
    """重置用户密码（管理员）"""
    if not request.user.is_admin:
        return Response({
            'success': False,
            'message': '权限不足'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        account = Account.objects.get(account_id=user_id)
        new_password = '123456'  # 默认密码
        account.set_password(new_password)
        account.save()
        
        return Response({
            'success': True,
            'message': f'密码重置成功，新密码为：{new_password}'
        })
    except Account.DoesNotExist:
        return Response({
            'success': False,
            'message': '用户不存在'
        }, status=status.HTTP_404_NOT_FOUND)


def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

