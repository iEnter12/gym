from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import uuid
from .models import WeatherData, ChatHistory
from .serializers import (
    WeatherDataSerializer, ChatHistorySerializer, ChatRequestSerializer
)
from .services import WeatherService, AIService


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def harbin_weather_view(request):
    """获取哈尔滨天气"""
    try:
        weather_service = WeatherService()
        weather_data = weather_service.get_weather('哈尔滨')
        
        # 保存到数据库（用于缓存和历史记录）
        # weather_obj, created = WeatherData.objects.update_or_create(
        #     city='哈尔滨',
        #     defaults=weather_data
        # )
        
        return Response({
            'success': True,
            'data': weather_data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取天气信息失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def ai_chat_view(request):
    """AI聊天"""
    serializer = ChatRequestSerializer(data=request.data)
    if serializer.is_valid():
        try:
            message = serializer.validated_data['message']
            session_id = serializer.validated_data.get('session_id') or str(uuid.uuid4())
            
            # 调用AI服务
            ai_service = AIService()
            ai_response = ai_service.chat(message, session_id)
            
            # 保存聊天历史
            chat_history = ChatHistory.objects.create(
                session_id=session_id,
                user_message=message,
                ai_response=ai_response
            )
            
            return Response({
                'success': True,
                'data': {
                    'session_id': session_id,
                    'message': ai_response,
                    'timestamp': chat_history.create_time.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'AI聊天失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'success': False,
        'message': 'AI聊天失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def chat_history_view(request):
    """获取聊天历史"""
    session_id = request.query_params.get('session_id')
    
    if not session_id:
        return Response({
            'success': False,
            'message': '请提供会话ID'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # 获取聊天历史
        chat_history = ChatHistory.objects.filter(
            session_id=session_id
        ).order_by('create_time')
        
        # 限制返回数量
        limit = int(request.query_params.get('limit', 50))
        chat_history = chat_history[:limit]
        
        history_data = []
        for chat in chat_history:
            history_data.append({
                'user_message': chat.user_message,
                'ai_response': chat.ai_response,
                'timestamp': chat.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return Response({
            'success': True,
            'data': {
                'session_id': session_id,
                'history': history_data
            }
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取聊天历史失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def weather_forecast_view(request):
    """获取天气预报（扩展功能）"""
    city = request.query_params.get('city', '哈尔滨')
    
    try:
        weather_service = WeatherService()
        weather_data = weather_service.get_weather(city)
        
        return Response({
            'success': True,
            'data': weather_data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取天气预报失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_status_view(request):
    """API状态检查（管理员）"""
    if not request.user.is_admin:
        return Response({
            'success': False,
            'message': '权限不足'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # 检查天气API状态
        weather_service = WeatherService()
        weather_status = 'available'
        try:
            weather_service.get_weather('哈尔滨')
        except:
            weather_status = 'unavailable'
        
        # 检查AI API状态
        ai_service = AIService()
        ai_status = 'available'
        try:
            ai_service.chat('测试')
        except:
            ai_status = 'unavailable'
        
        # 统计信息
        total_chats = ChatHistory.objects.count()
        today_chats = ChatHistory.objects.filter(
            create_time__date=timezone.now().date()
        ).count()
        
        weather_records = WeatherData.objects.count()
        
        return Response({
            'success': True,
            'data': {
                'weather_api': {
                    'status': weather_status,
                    'records': weather_records
                },
                'ai_api': {
                    'status': ai_status,
                    'total_chats': total_chats,
                    'today_chats': today_chats
                },
                'check_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'API状态检查失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

