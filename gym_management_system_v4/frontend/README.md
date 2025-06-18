# 体育场馆预约系统

一个现代化的体育场馆预约管理系统，采用蓝色主题设计，支持普通用户和管理员两种角色。

## 项目特点

- 🎨 **美观设计**: 采用现代化蓝色主题，界面简洁美观
- 📱 **响应式布局**: 支持桌面端和移动端访问
- 👥 **双角色支持**: 普通用户和管理员分别拥有不同功能
- 🔧 **易于集成**: 代码结构清晰，便于后端API集成
- 🎯 **功能完整**: 涵盖预约、会员、支付、评价等完整业务流程

## 技术栈

- **前端框架**: 原生HTML + CSS + JavaScript
- **UI组件库**: Element UI
- **HTTP请求**: Axios
- **日期处理**: Day.js
- **图表库**: ECharts
- **状态管理**: localStorage + sessionStorage

## 项目结构

```
sports-venue-system/
├── index.html                 # 登录页面
├── assets/                    # 静态资源
│   ├── css/                   # 样式文件
│   │   ├── common.css         # 通用样式
│   │   ├── login.css          # 登录页面样式
│   │   ├── user.css           # 用户端样式
│   │   └── admin.css          # 管理端样式
│   ├── images/                # 图片资源
│   └── js/                    # JavaScript文件
├── components/                # 组件目录
│   ├── common/                # 通用组件
│   ├── user/                  # 用户端组件
│   └── admin/                 # 管理端组件
├── pages/                     # 页面目录
│   ├── user/                  # 用户端页面
│   │   ├── home.html          # 用户首页
│   │   ├── facilities.html    # 场馆列表
│   │   ├── booking.html       # 预约详情
│   │   ├── profile.html       # 个人中心
│   │   └── ai-chat.html       # AI助手
│   └── admin/                 # 管理端页面
│       ├── dashboard.html     # 管理仪表盘
│       ├── facilities.html    # 场馆管理
│       ├── bookings.html      # 预约管理
│       ├── users.html         # 用户管理
│       └── statistics.html    # 统计报表
└── utils/                     # 工具类
    ├── api.js                 # API接口管理
    ├── auth.js                # 认证管理
    └── mock.js                # 模拟数据
```

## 功能模块

### 登录系统
- 支持普通用户和管理员登录
- 用户注册功能（仅限普通用户）
- 记住密码功能
- 公告栏显示

### 普通用户端
- **首页**: 轮播图、搜索栏、天气信息、热门场馆推荐
- **场馆列表**: 按类型筛选、搜索功能
- **预约详情**: 场馆信息、时间选择、预约表单、评价查看
- **个人中心**: 预约记录、会员状态、订单历史、个人信息
- **AI助手**: 体育相关问题咨询

### 管理员端
- **数据仪表盘**: 实时数据统计、图表展示
- **场馆管理**: 场馆CRUD操作、状态管理
- **预约管理**: 预约审核、状态更新
- **用户管理**: 用户信息管理、权限控制
- **统计报表**: 收入统计、使用率分析

## 后端集成指南

### API接口规范

所有API接口都在 `utils/api.js` 中定义，采用RESTful风格：

```javascript
// 基础配置
baseURL: '/api'
timeout: 10000
headers: { 'Content-Type': 'application/json' }

// 认证头
Authorization: 'Bearer {token}'
```

### 主要接口列表

#### 认证相关
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `GET /api/auth/user` - 获取用户信息
- `POST /api/auth/logout` - 退出登录

#### 场馆相关
- `GET /api/facilities` - 获取场馆列表
- `GET /api/facilities/{id}` - 获取场馆详情
- `GET /api/facility-types` - 获取场馆类型
- `POST /api/facilities` - 创建场馆（管理员）
- `PUT /api/facilities/{id}` - 更新场馆（管理员）

#### 预约相关
- `POST /api/bookings` - 创建预约
- `GET /api/bookings/user` - 获取用户预约
- `GET /api/bookings` - 获取所有预约（管理员）
- `PUT /api/bookings/{id}/cancel` - 取消预约

#### 会员相关
- `GET /api/membership-packages` - 获取会员套餐
- `POST /api/memberships` - 购买会员
- `GET /api/memberships/user` - 获取用户会员状态

### 数据库对应关系

前端数据结构与数据库表结构完全对应：

- `accounts` - 用户账户表
- `facilities` - 场馆表
- `facility_types` - 场馆类型表
- `bookings` - 预约表
- `orders` - 订单表
- `memberships` - 会员记录表
- `membership_packages` - 会员套餐表
- `reviews` - 评价表
- `notices` - 公告表

### 状态码规范

```javascript
// 预约状态
0: 未开始
1: 进行中
2: 已完成
3: 已取消
4: 已过期

// 用户类型
1: 普通用户
2: 管理员

// 用户状态
1: 正常
2: 禁用

// 支付状态
1: 待支付
2: 已支付
3: 已退款
```

### 模拟数据说明

项目包含完整的模拟数据系统（`utils/mock.js`），便于前端开发和测试：

- 自动生成测试用户和管理员账户
- 完整的场馆和预约数据
- 支持数据持久化（localStorage）
- 模拟真实API响应格式

### 替换为真实API

1. 修改 `utils/api.js` 中的 `baseURL`
2. 移除 `utils/mock.js` 的引用
3. 更新认证token处理逻辑
4. 调整错误处理机制

## 部署说明

### 开发环境
1. 直接用浏览器打开 `index.html`
2. 或使用本地服务器（如Live Server）

### 生产环境
1. 将整个项目文件夹部署到Web服务器
2. 配置反向代理指向后端API
3. 设置正确的API基础路径

## 浏览器兼容性

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 开发规范

### CSS规范
- 使用CSS变量定义主题色彩
- 采用BEM命名规范
- 响应式设计优先

### JavaScript规范
- 使用ES6+语法
- 模块化组织代码
- 统一错误处理

### 代码注释
- 关键功能添加中文注释
- API接口包含完整文档
- 复杂逻辑提供说明

## 测试账户

### 管理员账户
- 用户名: `admin`
- 密码: `123456`

### 普通用户账户
- 用户名: `user001`
- 密码: `123456`

## 联系方式

如有问题或建议，请联系开发团队。

