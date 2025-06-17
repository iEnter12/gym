# 体育馆管理系统 - 项目文档

## 项目概述

体育馆管理系统是一个基于Django后端和Vue.js前端的现代化场馆预约管理平台。系统提供用户注册登录、场馆预约、订单管理、评价系统、公告管理等核心功能，并集成了天气预报和AI智能客服等增值服务。

### 技术栈

**后端技术**：
- Django 4.2
- Django REST Framework
- SQLite3 / 达梦数据库
- Django ORM
- Token认证
- 内存缓存 / Redis

**前端技术**：
- Vue.js 2.x
- Element UI
- Axios
- Day.js

**第三方服务**：
- 易客天气API
- Free API AI聊天服务

### 项目特色

1. **完整的用户管理系统**：支持普通用户和管理员两种角色
2. **智能预约系统**：实时查看场馆可用时间，支持在线预约和支付
3. **评价反馈系统**：用户可对场馆进行评价，管理员可回复
4. **智能客服**：集成AI聊天机器人，提供24小时智能咨询
5. **天气服务**：实时显示哈尔滨天气信息，辅助用户决策
6. **响应式设计**：支持桌面端和移动端访问

## 系统架构

### 整体架构图

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端 (Vue.js)  │    │  后端 (Django)   │    │   数据库 (SQLite) │
│                 │    │                 │    │                 │
│ - 用户界面       │◄──►│ - RESTful API   │◄──►│ - 用户数据       │
│ - 状态管理       │    │ - 业务逻辑       │    │ - 业务数据       │
│ - 路由管理       │    │ - 数据验证       │    │ - 系统配置       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   第三方服务     │    │   缓存系统       │
│                 │    │                 │
│ - 天气API       │    │ - 内存缓存       │
│ - AI聊天API     │    │ - 会话缓存       │
└─────────────────┘    └─────────────────┘
```

### 数据库设计

系统采用关系型数据库设计，主要包含以下核心表：

1. **accounts** - 用户账户表
2. **facilities** - 场馆信息表
3. **facility_types** - 场馆类型表
4. **bookings** - 预约记录表
5. **orders** - 订单信息表
6. **reviews** - 评价信息表
7. **notices** - 公告信息表
8. **weather_data** - 天气数据表
9. **chat_history** - 聊天历史表

### API设计

系统采用RESTful API设计风格，主要模块包括：

- `/api/auth/` - 用户认证模块
- `/api/facilities/` - 场馆管理模块
- `/api/bookings/` - 预约管理模块
- `/api/orders/` - 订单管理模块
- `/api/reviews/` - 评价管理模块
- `/api/notices/` - 公告管理模块
- `/api/external/` - 第三方服务模块

## 功能模块详解

### 1. 用户管理模块

**功能特性**：
- 用户注册、登录、退出
- 用户资料管理
- 密码修改
- 用户状态管理（管理员功能）

**权限设计**：
- 普通用户：基础功能权限
- 管理员：全部管理权限

### 2. 场馆管理模块

**功能特性**：
- 场馆信息展示
- 场馆类型分类
- 场馆可用时间查询
- 场馆CRUD操作（管理员）

**业务规则**：
- 场馆按类型分类管理
- 支持图片上传和展示
- 实时显示可用状态

### 3. 预约管理模块

**功能特性**：
- 在线预约场馆
- 预约状态跟踪
- 预约取消和修改
- 预约统计分析（管理员）

**预约流程**：
1. 选择场馆和时间
2. 确认预约信息
3. 生成订单
4. 支付确认
5. 预约成功

### 4. 订单管理模块

**功能特性**：
- 订单生成和管理
- 支付状态跟踪
- 退款处理
- 收入统计（管理员）

**支付流程**：
- 支持多种支付方式
- 自动生成订单号
- 支付状态实时更新

### 5. 评价系统模块

**功能特性**：
- 用户评价场馆
- 评分和评论
- 管理员回复评价
- 评价统计分析

### 6. 公告管理模块

**功能特性**：
- 公告发布和管理
- 公告分类和置顶
- 公告有效期管理
- 公告浏览统计

### 7. 第三方服务模块

**天气服务**：
- 实时天气信息
- 天气预报
- 缓存优化

**AI客服**：
- 智能问答
- 会话管理
- 关键词识别
- 自动回复

## 部署指南

### 环境要求

**系统要求**：
- Python 3.8+
- Node.js 14+ (开发环境)
- 数据库：SQLite3 / 达梦数据库
- 缓存：内存缓存 / Redis

**Python依赖**：
```
Django==4.2
djangorestframework
django-cors-headers
python-decouple
requests
```

### 后端部署

1. **克隆项目代码**
```bash
git clone <repository_url>
cd gym_management_project
```

2. **安装Python依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库和第三方API密钥
```

4. **数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **创建超级用户**
```bash
python manage.py createsuperuser
```

6. **启动开发服务器**
```bash
python manage.py runserver 0.0.0.0:8000
```

### 前端部署

1. **进入前端目录**
```bash
cd frontend/fronted
```

2. **配置API地址**
编辑 `utils/api.js` 文件，修改 `baseURL` 为后端服务器地址。

3. **启动静态文件服务器**
```bash
python -m http.server 3000
```

### 生产环境部署

**推荐配置**：
- Web服务器：Nginx
- WSGI服务器：Gunicorn
- 数据库：达梦数据库
- 缓存：Redis
- 进程管理：Supervisor

**Nginx配置示例**：
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location / {
        root /path/to/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

## API文档

### 认证接口

#### 用户注册
```
POST /api/auth/register
Content-Type: application/json

{
    "username": "string",
    "password": "string",
    "confirm_password": "string",
    "real_name": "string",
    "phone": "string",
    "email": "string"
}
```

#### 用户登录
```
POST /api/auth/login
Content-Type: application/json

{
    "username": "string",
    "password": "string",
    "user_type": 1
}
```

### 场馆接口

#### 获取场馆列表
```
GET /api/facilities/
Authorization: Token <token>

Query Parameters:
- page: 页码
- page_size: 每页数量
- facility_type: 场馆类型
- search: 搜索关键词
```

#### 获取场馆详情
```
GET /api/facilities/{id}/
Authorization: Token <token>
```

### 预约接口

#### 创建预约
```
POST /api/bookings/create
Authorization: Token <token>
Content-Type: application/json

{
    "facility_id": 1,
    "booking_date": "2025-06-17",
    "start_time": "09:00",
    "end_time": "11:00",
    "purpose": "string"
}
```

#### 获取预约列表
```
GET /api/bookings/
Authorization: Token <token>

Query Parameters:
- status: 预约状态
- start_date: 开始日期
- end_date: 结束日期
```

### 第三方服务接口

#### 获取天气信息
```
GET /api/external/weather/harbin/

Response:
{
    "success": true,
    "data": {
        "city": "哈尔滨",
        "temperature": 18,
        "weather": "小雨",
        "icon": "rainy",
        "humidity": 56,
        "wind_speed": 5,
        "update_time": "2025-06-17 05:22:06"
    }
}
```

#### AI聊天
```
POST /api/external/ai/chat/
Content-Type: application/json

{
    "message": "string",
    "session_id": "string"
}

Response:
{
    "success": true,
    "data": {
        "session_id": "uuid",
        "message": "string",
        "timestamp": "2025-06-17 05:22:11"
    }
}
```

## 用户手册

### 普通用户操作指南

#### 1. 注册和登录
1. 访问系统首页
2. 选择"普通用户"标签
3. 点击"注册"填写个人信息
4. 注册成功后使用用户名和密码登录

#### 2. 浏览场馆
1. 登录后进入用户首页
2. 浏览场馆列表
3. 点击场馆查看详细信息
4. 查看场馆评价和图片

#### 3. 预约场馆
1. 选择心仪的场馆
2. 选择预约日期和时间
3. 填写预约用途
4. 确认预约信息
5. 完成支付

#### 4. 管理预约
1. 在"我的预约"中查看所有预约
2. 可以取消未开始的预约
3. 预约完成后可以进行评价

#### 5. 使用AI客服
1. 点击页面右下角的客服图标
2. 输入问题发送消息
3. AI客服会自动回复相关信息

### 管理员操作指南

#### 1. 管理员登录
1. 访问系统首页
2. 选择"管理员"标签
3. 使用管理员账号登录

#### 2. 场馆管理
1. 进入"场馆管理"页面
2. 可以添加、编辑、删除场馆
3. 设置场馆的开放时间和价格
4. 上传场馆图片

#### 3. 预约管理
1. 查看所有用户的预约记录
2. 确认或取消预约
3. 查看预约统计数据

#### 4. 用户管理
1. 查看所有注册用户
2. 可以禁用或启用用户账号
3. 重置用户密码

#### 5. 公告管理
1. 发布系统公告
2. 设置公告的有效期
3. 置顶重要公告

## 常见问题

### Q1: 如何配置第三方API密钥？
A: 编辑项目根目录的 `.env` 文件，添加以下配置：
```
WEATHER_API_APPID=your_weather_api_appid
WEATHER_API_SECRET=your_weather_api_secret
AI_API_KEY=your_ai_api_key
```

### Q2: 如何切换到达梦数据库？
A: 修改 `settings.py` 中的数据库配置：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django_dm',
        'NAME': 'gym_management',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5236',
    }
}
```

### Q3: 如何启用Redis缓存？
A: 修改 `settings.py` 中的缓存配置：
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Q4: 前端如何连接不同的后端地址？
A: 修改 `frontend/fronted/utils/api.js` 文件中的 `baseURL`：
```javascript
this.baseURL = 'http://your-backend-server:8000/api';
```

## 维护和更新

### 日志管理
系统日志存储在 `logs/django.log` 文件中，包含：
- 系统运行日志
- 错误日志
- 第三方API调用日志

### 数据备份
建议定期备份数据库：
```bash
# SQLite备份
cp db.sqlite3 backup/db_$(date +%Y%m%d).sqlite3

# 达梦数据库备份
# 使用达梦数据库的备份工具
```

### 性能监控
- 监控API响应时间
- 监控数据库查询性能
- 监控第三方服务可用性
- 监控系统资源使用情况

### 安全更新
- 定期更新Django和依赖包
- 检查安全漏洞
- 更新第三方API密钥
- 备份重要数据

## 技术支持

如有技术问题，请联系开发团队或查阅以下资源：

- Django官方文档：https://docs.djangoproject.com/
- Django REST Framework文档：https://www.django-rest-framework.org/
- Vue.js官方文档：https://vuejs.org/
- Element UI文档：https://element.eleme.io/

---

**项目版本**: 1.0.0  
**文档更新时间**: 2025-06-17  
**开发团队**: Manus AI

