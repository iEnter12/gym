import requests
import json
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta, datetime
import logging

logger = logging.getLogger(__name__)


class WeatherService:
    """天气服务类"""
    
    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY
        # self.api_url = "https://api.weatherapi.com/v1/forecast.json"
        self.api_url = "http://restapi.amap.com/v3/weather/weatherInfo"
        self.cache_timeout = 300  # 5分钟缓存
    
    def get_weather_forecast(self, city_code="230100", extensions="base"):
        try:
            # params = {
            #     'key': self.api_key,
            #     'q': city,
            #     'days': 3,
            #     'aqi': 'no',
            #     'alerts': 'no'
            # }
            params = {
                'key': self.api_key,
                'city': city_code,
                'extensions': extensions,
                'output': 'JSON'
            }
            print(self.api_key)
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"获取天气数据失败: {str(e)}")
            return None
    
    def get_weather(self, city='哈尔滨'):
        """获取天气信息"""
        cache_key = f'weather_{city}'

        
        # 尝试从缓存获取
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"从缓存获取天气数据: {city}")
            return cached_data
        
        try:
            # 调用真实API
            if self.api_key:
                logger.info(f"调用天气API获取数据: {city}")
                weather_data = self.get_weather_forecast(city_code=230100)
            else:
                logger.warning("未配置天气API密钥，使用模拟数据")
                weather_data = self._get_mock_weather(city)
            
            # 缓存数据
            cache.set(cache_key, weather_data, self.cache_timeout)
            logger.info(f"天气数据已缓存: {city}")
            return weather_data
            
        except Exception as e:
            logger.error(f"获取天气信息失败: {str(e)}")
            # 返回模拟数据作为备用
            logger.info("使用模拟数据作为备用")
            return self._get_mock_weather(city)
    
    def _get_mock_weather(self, city):
        """获取模拟天气数据"""
        import random
        import datetime
        
        # 根据季节生成合适的天气
        month = datetime.datetime.now().month
        
        if month in [12, 1, 2]:  # 冬季
            weather_options = [
                {'weather': '晴', 'icon': 'sunny', 'temp_range': (-10, 5)},
                {'weather': '雪', 'icon': 'snowy', 'temp_range': (-15, -2)},
                {'weather': '阴', 'icon': 'overcast', 'temp_range': (-8, 2)},
            ]
        elif month in [3, 4, 5]:  # 春季
            weather_options = [
                {'weather': '晴', 'icon': 'sunny', 'temp_range': (8, 18)},
                {'weather': '多云', 'icon': 'cloudy', 'temp_range': (5, 15)},
                {'weather': '小雨', 'icon': 'rainy', 'temp_range': (3, 12)},
            ]
        elif month in [6, 7, 8]:  # 夏季
            weather_options = [
                {'weather': '晴', 'icon': 'sunny', 'temp_range': (20, 30)},
                {'weather': '多云', 'icon': 'cloudy', 'temp_range': (18, 28)},
                {'weather': '小雨', 'icon': 'rainy', 'temp_range': (15, 25)},
            ]
        else:  # 秋季
            weather_options = [
                {'weather': '晴', 'icon': 'sunny', 'temp_range': (10, 20)},
                {'weather': '多云', 'icon': 'cloudy', 'temp_range': (8, 18)},
                {'weather': '阴', 'icon': 'overcast', 'temp_range': (5, 15)},
            ]
        
        weather_info = random.choice(weather_options)
        temp_min, temp_max = weather_info['temp_range']
        temperature = random.randint(temp_min, temp_max)
        
        return {
            'city': city,
            'temperature': temperature,
            'weather': weather_info['weather'],
            'icon': weather_info['icon'],
            'humidity': random.randint(40, 80),
            'windSpeed': random.randint(1, 5),
            'updateTime': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }


class AIService:
    """AI聊天服务类"""
    
    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.api_url = settings.AI_API_URL
    
    def get_ai_response(self, prompt, max_tokens=150):
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-chat",  # 使用DeepSeek-V3-0324模型
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens
            }
            response = requests.post(self.api_url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"获取AI响应失败: {str(e)}")
            return None
    
    def chat(self, message, session_id=None):
        """处理聊天请求并返回AI回复"""
        try:
            # 如果有会话ID，可以在这里处理上下文
            context = f"用户ID: {session_id}\n" if session_id else ""
            
            # 构建提示词
            prompt = f"{context}用户: {message}\n请针对体育场馆预约系统的用户提供专业、友好的回复。"
            
            # 调用AI API获取回复
            response_data = self.get_ai_response(prompt, max_tokens=300)
            
            # 解析回复
            if response_data and 'choices' in response_data and len(response_data['choices']) > 0:
                ai_message = response_data['choices'][0]['message']['content'].strip()
                return ai_message
            else:
                # 如果API调用失败，返回默认回复
                return "抱歉，我暂时无法回答您的问题。请稍后再试。"
                
        except Exception as e:
            logger.error(f"AI聊天处理失败: {str(e)}")
            return "系统繁忙，请稍后再试。"


# PaymentService已删除


class NotificationService:
    def __init__(self):
        self.api_key = settings.NOTIFICATION_API_KEY
        self.api_url = "https://api.notification.com/v1/messages"
    
    def send_notification(self, user_id, title, content, notification_type="system"):
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "user_id": user_id,
                "title": title,
                "content": content,
                "type": notification_type,
                "timestamp": datetime.now().isoformat()
            }
            response = requests.post(self.api_url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"发送通知失败: {str(e)}")
            return None

