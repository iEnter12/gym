# API集成配置文档

## 基础配置

### 服务器配置
```
基础URL: /api
超时时间: 10000ms
内容类型: application/json
认证方式: Bearer Token
```

### 请求头配置
```javascript
{
  "Content-Type": "application/json",
  "Authorization": "Bearer {token}",
  "Accept": "application/json"
}
```

## 响应格式规范

### 成功响应
```javascript
{
  "success": true,
  "data": {}, // 具体数据
  "message": "操作成功",
  "timestamp": "2024-06-13T10:00:00Z"
}
```

### 错误响应
```javascript
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述",
    "details": {}
  },
  "timestamp": "2024-06-13T10:00:00Z"
}
```

## 认证接口

### 用户登录
```
POST /api/auth/login
Content-Type: application/json

请求体:
{
  "username": "string",     // 用户名或手机号
  "password": "string",     // 密码
  "userType": 1            // 1:普通用户 2:管理员
}

响应:
{
  "success": true,
  "data": {
    "token": "jwt_token_string",
    "user": {
      "account_id": 1,
      "username": "user001",
      "real_name": "张三",
      "phone": "13800138001",
      "email": "user@example.com",
      "avatar": "avatar_url",
      "user_type": 1,
      "status": 1
    }
  }
}
```

### 用户注册
```
POST /api/auth/register
Content-Type: application/json

请求体:
{
  "username": "string",
  "password": "string",
  "realName": "string",
  "phone": "string",
  "email": "string"
}
```

## 场馆接口

### 获取场馆列表
```
GET /api/facilities?type_id=1&status=1&keyword=篮球

查询参数:
- type_id: 场馆类型ID（可选）
- status: 场馆状态（可选）
- keyword: 搜索关键词（可选）
- page: 页码（可选，默认1）
- limit: 每页数量（可选，默认10）

响应:
{
  "success": true,
  "data": {
    "list": [
      {
        "facility_id": 1,
        "type_id": 1,
        "facility_name": "1号篮球场",
        "location": "体育馆一楼东侧",
        "capacity": 20,
        "area": 420.00,
        "image_url": "/images/basketball-1.jpg",
        "price": 80.00,
        "description": "标准篮球场...",
        "status": 1,
        "type_name": "篮球场"
      }
    ],
    "total": 100,
    "page": 1,
    "limit": 10
  }
}
```

### 获取场馆详情
```
GET /api/facilities/{id}

响应:
{
  "success": true,
  "data": {
    "facility_id": 1,
    "type_id": 1,
    "facility_name": "1号篮球场",
    "location": "体育馆一楼东侧",
    "capacity": 20,
    "area": 420.00,
    "image_url": "/images/basketball-1.jpg",
    "price": 80.00,
    "description": "标准篮球场...",
    "status": 1,
    "create_time": "2024-01-01 10:00:00",
    "update_time": "2024-01-01 10:00:00",
    "type_info": {
      "type_id": 1,
      "type_name": "篮球场",
      "icon": "el-icon-basketball"
    }
  }
}
```

## 预约接口

### 创建预约
```
POST /api/bookings
Content-Type: application/json
Authorization: Bearer {token}

请求体:
{
  "facility_id": 1,
  "booking_date": "2024-06-15",
  "start_time": "09:00",
  "end_time": "11:00",
  "person_count": 4,
  "remark": "朋友聚会",
  "is_member_used": 0
}

响应:
{
  "success": true,
  "data": {
    "booking_id": 123,
    "order_no": "ORD20240613001",
    "total_amount": 160.00,
    "actual_amount": 160.00
  }
}
```

### 获取用户预约列表
```
GET /api/bookings/user?status=0&page=1&limit=10
Authorization: Bearer {token}

查询参数:
- status: 预约状态（可选）
- date: 预约日期（可选）
- page: 页码（可选）
- limit: 每页数量（可选）
```

## 会员接口

### 获取会员套餐
```
GET /api/membership-packages

响应:
{
  "success": true,
  "data": [
    {
      "package_id": 1,
      "package_name": "月卡",
      "price": 299.00,
      "duration_days": 30,
      "discount": 0.9,
      "monthly_free_times": 10,
      "description": "每月10次免费使用，其他时间9折优惠"
    }
  ]
}
```

### 购买会员
```
POST /api/memberships
Content-Type: application/json
Authorization: Bearer {token}

请求体:
{
  "package_id": 1,
  "payment_method": 1  // 1:微信 2:支付宝 3:现金
}
```

## 订单接口

### 创建订单
```
POST /api/orders
Content-Type: application/json
Authorization: Bearer {token}

请求体:
{
  "booking_id": 123,
  "order_type": 1,        // 1:预约支付 2:会员购买
  "payment_method": 1     // 1:微信 2:支付宝 3:现金
}
```

### 支付订单
```
POST /api/orders/{id}/pay
Content-Type: application/json
Authorization: Bearer {token}

请求体:
{
  "payment_method": 1,
  "payment_info": {}  // 支付相关信息
}
```

## 评价接口

### 创建评价
```
POST /api/reviews
Content-Type: application/json
Authorization: Bearer {token}

请求体:
{
  "facility_id": 1,
  "booking_id": 123,
  "rating": 5,
  "content": "场馆很不错，设施完善",
  "images": ["image1.jpg", "image2.jpg"]
}
```

## 统计接口（管理员）

### 获取仪表盘数据
```
GET /api/statistics/dashboard
Authorization: Bearer {token}

响应:
{
  "success": true,
  "data": {
    "today_bookings": 25,
    "today_revenue": 2000.00,
    "total_users": 1500,
    "active_members": 300,
    "facility_usage_rate": 0.75,
    "recent_bookings": [],
    "revenue_chart": [],
    "popular_facilities": []
  }
}
```

## 错误码说明

```
400 - 请求参数错误
401 - 未授权访问
403 - 权限不足
404 - 资源不存在
409 - 数据冲突（如时间冲突）
422 - 数据验证失败
500 - 服务器内部错误
```

## 数据验证规则

### 用户注册
- username: 3-20字符，字母数字下划线
- password: 6-20字符
- phone: 11位手机号
- email: 有效邮箱格式（可选）

### 预约创建
- booking_date: 不能早于当前日期
- start_time/end_time: 营业时间内（6:00-22:00）
- person_count: 不超过场馆容量

## 文件上传

### 头像上传
```
POST /api/upload/avatar
Content-Type: multipart/form-data
Authorization: Bearer {token}

表单数据:
file: 图片文件（jpg/png，最大2MB）

响应:
{
  "success": true,
  "data": {
    "url": "/uploads/avatars/user_123_20240613.jpg"
  }
}
```

## 实时通知

### WebSocket连接
```
ws://localhost:8080/ws?token={jwt_token}

消息格式:
{
  "type": "booking_status_change",
  "data": {
    "booking_id": 123,
    "status": 1,
    "message": "您的预约已确认"
  }
}
```

## 缓存策略

### Redis缓存键
- `user:{user_id}` - 用户信息缓存（30分钟）
- `facility:{facility_id}` - 场馆信息缓存（1小时）
- `booking_slots:{facility_id}:{date}` - 可用时段缓存（10分钟）

## 安全考虑

1. 所有API都需要HTTPS
2. JWT Token有效期24小时
3. 敏感操作需要二次验证
4. 限制API调用频率
5. 输入数据严格验证和过滤

