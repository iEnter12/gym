# 体育馆管理系统 - 快速开始指南

## 项目简介

这是一个基于Django + Vue.js的体育馆管理系统，提供场馆预约、用户管理、订单处理、评价系统等功能，并集成了天气预报和AI客服服务。

## 快速部署

### 1. 环境准备
```bash
# 确保已安装Python 3.8+
python --version

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库初始化
```bash
# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建管理员账号
python manage.py createsuperuser
```

### 3. 启动服务
```bash
# 启动后端服务器
python manage.py runserver 0.0.0.0:8000

# 启动前端服务器（新终端）
cd frontend/fronted
python -m http.server 3000
```

### 4. 访问系统
- 前端页面：http://localhost:3000
- 后端API：http://localhost:8000/api/
- 管理后台：http://localhost:8000/admin/

## 默认账号

**管理员账号**：
- 用户名：admin
- 密码：（创建时设置）

**测试用户**：
- 用户名：testuser
- 密码：123456

## 主要功能

✅ 用户注册登录  
✅ 场馆浏览预约  
✅ 订单管理支付  
✅ 评价反馈系统  
✅ 公告管理  
✅ 天气信息显示  
✅ AI智能客服  
✅ 管理员后台  

## 技术栈

- **后端**: Django 4.2 + Django REST Framework
- **前端**: Vue.js 2.x + Element UI
- **数据库**: SQLite3 (可切换达梦数据库)
- **缓存**: 内存缓存 (可切换Redis)

## 项目结构

```
gym_management_project/
├── gym_backend/          # Django项目配置
├── accounts/             # 用户管理应用
├── facilities/           # 场馆管理应用
├── bookings/            # 预约管理应用
├── orders/              # 订单管理应用
├── reviews/             # 评价管理应用
├── notices/             # 公告管理应用
├── external_apis/       # 第三方服务应用
├── frontend/fronted/    # 前端代码
├── db.sqlite3          # 数据库文件
├── requirements.txt    # Python依赖
└── README.md          # 详细文档
```

## 配置说明

### 第三方API配置
复制 `.env.example` 为 `.env`，配置以下参数：

```bash
# 天气API
WEATHER_API_APPID=your_appid
WEATHER_API_SECRET=your_secret

# AI聊天API
AI_API_KEY=your_key
```

### 数据库配置
默认使用SQLite3，生产环境可切换为达梦数据库。

### 缓存配置
默认使用内存缓存，生产环境建议使用Redis。

## 常见问题

1. **端口被占用**：修改启动命令中的端口号
2. **API连接失败**：检查前端API配置地址
3. **第三方服务异常**：系统会自动切换到模拟数据

## 更多信息

详细文档请查看 `README.md` 文件。

---
开发团队：Manus AI  
项目版本：1.0.0

