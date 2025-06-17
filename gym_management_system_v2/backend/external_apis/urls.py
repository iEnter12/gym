from django.urls import path
from . import views

urlpatterns = [
    # 天气API
    path('weather/harbin/', views.harbin_weather_view, name='harbin_weather'),
    path('weather/forecast/', views.weather_forecast_view, name='weather_forecast'),
    
    # AI聊天API
    path('ai/chat/', views.ai_chat_view, name='ai_chat'),
    path('ai/history/', views.chat_history_view, name='chat_history'),
    
    # API状态检查
    path('status/', views.api_status_view, name='api_status'),
]

