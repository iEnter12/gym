# 前端修改说明文档

## 主要修改内容

### 1. API配置更新
- 更新 `utils/api.js` 中的 `baseURL` 为 Django 后端地址
- 修改认证方式从 `Bearer` token 改为 `Token` token
- 调整响应数据处理逻辑以适配 Django 后端返回格式

### 2. 认证系统更新
- 更新 `utils/auth.js` 中的用户信息处理逻辑
- 添加 `handleLoginSuccess` 方法处理登录成功响应
- 移除会员相关权限检查（功能已下线）

### 3. 需要修改的页面

#### 3.1 登录页面 (index.html)
- 将模拟登录替换为真实API调用
- 更新注册逻辑
- 修改公告加载逻辑

#### 3.2 用户首页 (pages/user/home.html)
- 更新天气数据获取
- 修改场馆列表加载
- 更新AI聊天功能

#### 3.3 管理员仪表盘 (pages/admin/dashboard.html)
- 更新统计数据获取
- 修改图表数据源

#### 3.4 场馆管理页面
- 更新CRUD操作
- 修改数据验证逻辑

#### 3.5 预约管理页面
- 更新预约列表获取
- 修改状态更新逻辑

### 4. 数据格式调整

#### 4.1 用户数据格式
```javascript
// 旧格式
{
  id: 1,
  username: 'user1',
  userType: 1
}

// 新格式（Django后端）
{
  account_id: 1,
  username: 'user1',
  user_type: 1,
  real_name: '张三',
  phone: '13800138000',
  email: 'user@example.com'
}
```

#### 4.2 响应数据格式
```javascript
// 旧格式
{
  code: 200,
  data: {...},
  message: 'success'
}

// 新格式（Django后端）
{
  success: true,
  data: {...},
  message: 'success'
}
```

### 5. 错误处理更新
- 统一错误消息显示
- 添加网络错误处理
- 更新权限验证逻辑

### 6. 第三方服务集成
- 天气API调用更新
- AI聊天接口调用更新
- 添加会话管理

## 修改优先级

1. **高优先级**：登录认证系统
2. **中优先级**：核心业务功能（场馆、预约）
3. **低优先级**：统计图表、第三方服务

## 测试要点

1. 用户登录注册功能
2. 权限验证和页面跳转
3. 数据CRUD操作
4. 第三方服务调用
5. 错误处理和用户体验

