# 体育馆管理项目数据库结构设计文档

## 项目概述

本文档基于前端代码分析和原始数据库表结构，设计了适配前端需求的修改后数据库结构。项目是一个体育馆管理系统，包含用户管理、场馆预约、订单支付、评价系统、公告管理等核心功能。

## 前端需求分析

通过对前端代码的深入分析，发现系统具有以下主要功能模块：

### 用户认证模块
前端支持普通用户和管理员两种角色的登录注册。用户可以通过用户名或手机号登录，注册时需要提供用户名、手机号、密码、真实姓名和邮箱（可选）。系统支持"记住我"功能，可以保存用户的登录凭据。

### 场馆管理模块
系统支持多种类型的体育场馆，包括篮球场、羽毛球场、游泳池、乒乓球室、健身房等。每个场馆都有详细的信息，包括名称、位置、容量、面积、价格、描述、状态等。场馆按类型进行分类管理，支持按类型、状态、关键词进行筛选和搜索。

### 预约系统模块
用户可以预约场馆，选择日期、时间段、人数等信息。系统需要检查时间冲突，确保同一场馆在同一时间段不会被重复预约。预约有多种状态：未开始、进行中、已完成、已取消、已过期。

### 订单支付模块
每个预约都会生成对应的订单，支持多种支付方式（微信、支付宝、现金）。订单包含原价、优惠金额、实际支付金额等信息。

### 评价系统模块
用户可以对已完成的预约进行评价，包括评分（1-5分）、评价内容、评价图片等。每个预约只能评价一次。

### 公告管理模块
系统支持发布各种类型的公告，包括系统公告、营业时间通知、活动通知等。公告有发布时间和结束时间，可以控制显示期间。

### 会员系统模块（已下线）
从前端代码分析发现，原本设计了会员系统，但在实际实现中已经下线。相关的API调用都返回空数据或错误信息。因此在数据库设计中，会员相关的表结构将保留但标记为已停用。

### 天气预报模块
前端集成了哈尔滨地区的天气预报功能，显示当前温度、天气状况、湿度、风速等信息。

### AI聊天模块
系统集成了AI聊天功能，用户可以与AI助手进行对话，获取运动建议和场馆相关信息。

## 原始数据库结构分析

原始数据库设计包含以下主要表：

1. **accounts表** - 存储用户和管理员信息
2. **facility_types表** - 定义场馆类别
3. **facilities表** - 存储场馆基本信息
4. **membership_packages表** - 会员套餐定义（已停用）
5. **memberships表** - 会员记录（已停用）
6. **bookings表** - 预约记录
7. **orders表** - 订单信息
8. **reviews表** - 评价记录
9. **notices表** - 公告信息

原始设计整体结构合理，表间关系清晰，但需要根据前端实际需求进行一些调整和优化。

## 修改后的数据库结构设计

基于前端需求分析和原始数据库结构，以下是修改后的数据库表结构设计：



### 1. 用户账户表 (accounts)

用户账户表是系统的核心表之一，存储所有用户（包括普通用户和管理员）的基本信息。表名使用`accounts`而非`user`或`users`，避免与数据库关键字冲突。

```sql
CREATE TABLE accounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '账户ID，主键',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名，唯一',
    password VARCHAR(255) NOT NULL COMMENT '密码，建议使用bcrypt加密',
    real_name VARCHAR(50) COMMENT '真实姓名',
    id_card VARCHAR(20) COMMENT '身份证号',
    phone VARCHAR(20) NOT NULL UNIQUE COMMENT '手机号，唯一',
    email VARCHAR(100) COMMENT '邮箱地址',
    avatar VARCHAR(255) COMMENT '头像URL',
    register_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    last_login_time DATETIME COMMENT '最后登录时间',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '账户状态：1-正常，2-禁用',
    user_type TINYINT NOT NULL DEFAULT 1 COMMENT '用户类型：1-普通用户，2-管理员',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_username (username),
    INDEX idx_phone (phone),
    INDEX idx_user_type (user_type),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户账户表';
```

**主要修改说明：**
- 密码字段长度增加到255，支持更强的加密算法
- 添加了必要的索引以提高查询性能
- 完善了字段注释，提高可维护性

### 2. 场馆类型表 (facility_types)

场馆类型表定义了系统支持的各种体育场馆类型，为场馆分类管理提供基础数据。

```sql
CREATE TABLE facility_types (
    type_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '类型ID，主键',
    type_name VARCHAR(50) NOT NULL UNIQUE COMMENT '类型名称，唯一',
    icon VARCHAR(255) COMMENT '类型图标CSS类名或图片URL',
    description VARCHAR(255) COMMENT '类型描述',
    sort_order INT DEFAULT 0 COMMENT '排序顺序，数字越小越靠前',
    is_active TINYINT NOT NULL DEFAULT 1 COMMENT '是否启用：1-启用，0-禁用',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    INDEX idx_sort_order (sort_order),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='场馆类型表';
```

**主要修改说明：**
- 添加了`sort_order`字段，支持自定义排序
- 添加了`is_active`字段，支持类型的启用/禁用管理
- 优化了索引设计

### 3. 场馆信息表 (facilities)

场馆信息表存储具体场馆的详细信息，是预约系统的核心数据表。

```sql
CREATE TABLE facilities (
    facility_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '场馆ID，主键',
    type_id INT NOT NULL COMMENT '场馆类型ID，外键',
    facility_name VARCHAR(100) NOT NULL COMMENT '场馆名称',
    location VARCHAR(255) NOT NULL COMMENT '场馆位置',
    capacity INT NOT NULL COMMENT '容纳人数',
    area DECIMAL(10,2) COMMENT '面积（平方米）',
    image_url VARCHAR(500) COMMENT '场馆图片URL',
    price DECIMAL(10,2) NOT NULL COMMENT '单价（元/小时）',
    description TEXT COMMENT '场馆描述',
    opening_hours VARCHAR(100) DEFAULT '06:00-22:00' COMMENT '营业时间',
    advance_booking_days INT DEFAULT 7 COMMENT '可提前预约天数',
    min_booking_duration INT DEFAULT 1 COMMENT '最小预约时长（小时）',
    max_booking_duration INT DEFAULT 4 COMMENT '最大预约时长（小时）',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '场馆状态：1-可用，2-维护中，3-已关闭',
    sort_order INT DEFAULT 0 COMMENT '排序顺序',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (type_id) REFERENCES facility_types(type_id),
    INDEX idx_type_id (type_id),
    INDEX idx_status (status),
    INDEX idx_sort_order (sort_order),
    INDEX idx_price (price)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='场馆信息表';
```

**主要修改说明：**
- 增加了营业时间、预约规则等业务字段
- 图片URL字段长度增加，支持更长的URL
- 添加了排序字段，支持场馆展示顺序管理
- 完善了索引设计，提高查询效率

### 4. 预约记录表 (bookings)

预约记录表是系统的核心业务表，记录用户的场馆预约信息和状态流转。

```sql
CREATE TABLE bookings (
    booking_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '预约ID，主键',
    account_id INT NOT NULL COMMENT '用户ID，外键',
    facility_id INT NOT NULL COMMENT '场馆ID，外键',
    booking_date DATE NOT NULL COMMENT '预约日期',
    start_time TIME NOT NULL COMMENT '开始时间',
    end_time TIME NOT NULL COMMENT '结束时间',
    person_count INT NOT NULL DEFAULT 1 COMMENT '预约人数',
    total_amount DECIMAL(10,2) NOT NULL COMMENT '总金额',
    status TINYINT NOT NULL DEFAULT 0 COMMENT '预约状态：0-未开始，1-进行中，2-已完成，3-已取消，4-已过期',
    remark VARCHAR(500) COMMENT '备注信息',
    is_member_used TINYINT DEFAULT 0 COMMENT '是否使用会员权益：1-是，0-否（已停用）',
    cancel_reason VARCHAR(255) COMMENT '取消原因',
    cancel_time DATETIME COMMENT '取消时间',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (facility_id) REFERENCES facilities(facility_id),
    INDEX idx_account_id (account_id),
    INDEX idx_facility_id (facility_id),
    INDEX idx_booking_date (booking_date),
    INDEX idx_status (status),
    INDEX idx_facility_date_time (facility_id, booking_date, start_time, end_time),
    UNIQUE KEY uk_facility_datetime (facility_id, booking_date, start_time, end_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='预约记录表';
```

**主要修改说明：**
- 添加了`total_amount`字段，直接存储预约总金额
- 增加了取消相关字段，完善取消流程管理
- 添加了唯一约束，防止同一时段重复预约
- 优化了复合索引，提高时间冲突检查效率

### 5. 订单信息表 (orders)

订单信息表记录所有的支付订单，与预约记录关联，支持多种支付方式。

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '订单ID，主键',
    order_no VARCHAR(50) NOT NULL UNIQUE COMMENT '订单号，唯一',
    account_id INT NOT NULL COMMENT '用户ID，外键',
    booking_id INT COMMENT '预约ID，外键（可为空，支持其他类型订单）',
    order_type TINYINT NOT NULL COMMENT '订单类型：1-预约支付，2-会员购买（已停用）',
    order_amount DECIMAL(10,2) NOT NULL COMMENT '订单原价',
    discount_amount DECIMAL(10,2) DEFAULT 0 COMMENT '优惠金额',
    actual_amount DECIMAL(10,2) NOT NULL COMMENT '实际支付金额',
    payment_method TINYINT COMMENT '支付方式：1-微信，2-支付宝，3-现金，4-银行卡',
    payment_status TINYINT NOT NULL DEFAULT 1 COMMENT '支付状态：1-待支付，2-已支付，3-已退款，4-支付失败',
    payment_time DATETIME COMMENT '支付时间',
    payment_no VARCHAR(100) COMMENT '第三方支付流水号',
    refund_amount DECIMAL(10,2) DEFAULT 0 COMMENT '退款金额',
    refund_time DATETIME COMMENT '退款时间',
    refund_reason VARCHAR(255) COMMENT '退款原因',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    INDEX idx_account_id (account_id),
    INDEX idx_booking_id (booking_id),
    INDEX idx_order_no (order_no),
    INDEX idx_payment_status (payment_status),
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单信息表';
```

**主要修改说明：**
- 完善了支付和退款相关字段
- 添加了第三方支付流水号字段
- 支持多种支付方式
- 优化了索引设计，提高订单查询效率

### 6. 评价记录表 (reviews)

评价记录表存储用户对场馆的评价信息，支持评分、文字评价和图片评价。

```sql
CREATE TABLE reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '评价ID，主键',
    account_id INT NOT NULL COMMENT '用户ID，外键',
    facility_id INT NOT NULL COMMENT '场馆ID，外键',
    booking_id INT NOT NULL COMMENT '预约ID，外键',
    rating TINYINT NOT NULL COMMENT '评分（1-5分）',
    content VARCHAR(1000) COMMENT '评价内容',
    images TEXT COMMENT '评价图片URL，JSON格式存储',
    reply_content VARCHAR(500) COMMENT '管理员回复内容',
    reply_time DATETIME COMMENT '回复时间',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '评价状态：1-已发布，2-已删除，3-已隐藏',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (facility_id) REFERENCES facilities(facility_id),
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    UNIQUE KEY uk_booking_id (booking_id),
    INDEX idx_account_id (account_id),
    INDEX idx_facility_id (facility_id),
    INDEX idx_rating (rating),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评价记录表';
```

**主要修改说明：**
- 增加了管理员回复功能
- 评价内容长度增加，支持更详细的评价
- 图片存储改为JSON格式，支持多张图片
- 添加了唯一约束，确保每个预约只能评价一次

### 7. 公告信息表 (notices)

公告信息表存储系统公告、活动通知等信息，支持定时发布和自动下线。

```sql
CREATE TABLE notices (
    notice_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '公告ID，主键',
    title VARCHAR(200) NOT NULL COMMENT '公告标题',
    content TEXT NOT NULL COMMENT '公告内容',
    notice_type TINYINT NOT NULL DEFAULT 1 COMMENT '公告类型：1-系统公告，2-营业时间，3-活动通知，4-维护通知',
    priority TINYINT DEFAULT 1 COMMENT '优先级：1-普通，2-重要，3-紧急',
    start_time DATETIME NOT NULL COMMENT '开始显示时间',
    end_time DATETIME COMMENT '结束显示时间',
    is_published TINYINT NOT NULL DEFAULT 1 COMMENT '发布状态：1-已发布，0-草稿',
    is_top TINYINT DEFAULT 0 COMMENT '是否置顶：1-置顶，0-普通',
    view_count INT DEFAULT 0 COMMENT '查看次数',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_notice_type (notice_type),
    INDEX idx_is_published (is_published),
    INDEX idx_start_time (start_time),
    INDEX idx_end_time (end_time),
    INDEX idx_is_top (is_top),
    INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='公告信息表';
```

**主要修改说明：**
- 增加了优先级和置顶功能
- 添加了查看次数统计
- 标题长度增加，支持更长的标题
- 完善了时间管理和状态控制

### 8. 会员套餐表 (membership_packages) - 已停用

虽然会员功能已停用，但保留表结构以备将来可能的功能恢复。

```sql
CREATE TABLE membership_packages (
    package_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '套餐ID，主键',
    package_name VARCHAR(100) NOT NULL COMMENT '套餐名称',
    price DECIMAL(10,2) NOT NULL COMMENT '价格（元）',
    duration_days INT NOT NULL COMMENT '有效期（天）',
    discount DECIMAL(5,2) NOT NULL DEFAULT 1.0 COMMENT '折扣率（1.0=无折扣）',
    monthly_free_times INT DEFAULT 0 COMMENT '每月免费次数（0=无限次）',
    description VARCHAR(500) COMMENT '套餐描述',
    is_active TINYINT NOT NULL DEFAULT 0 COMMENT '是否启用：1-启用，0-停用',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员套餐表（已停用）';
```

### 9. 会员记录表 (memberships) - 已停用

```sql
CREATE TABLE memberships (
    membership_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '会员记录ID，主键',
    account_id INT NOT NULL COMMENT '用户ID，外键',
    package_id INT NOT NULL COMMENT '套餐ID，外键',
    start_time DATETIME NOT NULL COMMENT '开始时间',
    end_time DATETIME NOT NULL COMMENT '结束时间',
    used_monthly_times INT DEFAULT 0 COMMENT '当月已使用免费次数',
    status TINYINT NOT NULL DEFAULT 3 COMMENT '会员状态：1-有效，2-已过期，3-已取消',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (package_id) REFERENCES membership_packages(package_id),
    INDEX idx_account_id (account_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员记录表（已停用）';
```

## 新增表结构

为了更好地支持前端功能和系统扩展，新增以下表结构：

### 10. 系统配置表 (system_configs)

```sql
CREATE TABLE system_configs (
    config_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '配置ID，主键',
    config_key VARCHAR(100) NOT NULL UNIQUE COMMENT '配置键名',
    config_value TEXT COMMENT '配置值',
    config_type VARCHAR(20) DEFAULT 'string' COMMENT '配置类型：string,number,boolean,json',
    description VARCHAR(255) COMMENT '配置描述',
    is_public TINYINT DEFAULT 0 COMMENT '是否公开：1-公开，0-私有',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_config_key (config_key),
    INDEX idx_is_public (is_public)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';
```

### 11. 操作日志表 (operation_logs)

```sql
CREATE TABLE operation_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '日志ID，主键',
    account_id INT COMMENT '操作用户ID，外键',
    operation_type VARCHAR(50) NOT NULL COMMENT '操作类型',
    operation_desc VARCHAR(255) COMMENT '操作描述',
    request_url VARCHAR(255) COMMENT '请求URL',
    request_method VARCHAR(10) COMMENT '请求方法',
    request_params TEXT COMMENT '请求参数',
    response_status INT COMMENT '响应状态码',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent VARCHAR(500) COMMENT '用户代理',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    INDEX idx_account_id (account_id),
    INDEX idx_operation_type (operation_type),
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表';
```

## 数据库初始化数据

为了系统正常运行，需要插入一些初始化数据：

### 场馆类型初始数据

```sql
INSERT INTO facility_types (type_name, icon, description, sort_order) VALUES
('篮球场', 'el-icon-basketball', '标准篮球场地，适合篮球运动', 1),
('羽毛球场', 'el-icon-badminton', '专业羽毛球场地，设施完善', 2),
('游泳池', 'el-icon-swimming', '标准游泳池，水质清洁', 3),
('乒乓球室', 'el-icon-ping-pong', '室内乒乓球场地，环境舒适', 4),
('健身房', 'el-icon-fitness', '现代化健身设备，专业指导', 5);
```

### 管理员账户初始数据

```sql
INSERT INTO accounts (username, password, real_name, phone, email, user_type) VALUES
('admin', '$2b$12$hash_password_here', '系统管理员', '13800138000', 'admin@example.com', 2);
```

### 系统配置初始数据

```sql
INSERT INTO system_configs (config_key, config_value, config_type, description, is_public) VALUES
('site_name', '体育场馆预约系统', 'string', '网站名称', 1),
('site_description', '智能化场馆预约平台', 'string', '网站描述', 1),
('booking_advance_days', '7', 'number', '可提前预约天数', 1),
('weather_api_key', '', 'string', '天气API密钥', 0),
('ai_api_key', '', 'string', 'AI接口密钥', 0);
```

## 索引优化策略

为了提高数据库查询性能，采用以下索引优化策略：

1. **主键索引**：所有表都使用自增主键，确保插入性能
2. **唯一索引**：用户名、手机号、订单号等唯一字段建立唯一索引
3. **外键索引**：所有外键字段建立索引，提高关联查询性能
4. **复合索引**：针对常用的多字段查询建立复合索引
5. **业务索引**：根据业务查询需求建立相应索引

## 数据库性能优化建议

1. **分区策略**：对于日志表等数据量大的表，可考虑按时间分区
2. **读写分离**：在高并发场景下，可配置主从复制实现读写分离
3. **缓存策略**：使用Redis缓存热点数据，减少数据库压力
4. **定期维护**：定期分析表结构，优化索引，清理过期数据

## 数据安全与备份策略

1. **数据加密**：敏感数据如密码使用强加密算法
2. **访问控制**：严格控制数据库访问权限
3. **定期备份**：建立自动备份机制，确保数据安全
4. **审计日志**：记录所有数据库操作，便于问题追踪

这个修改后的数据库结构设计充分考虑了前端需求，保持了原有设计的合理性，同时增加了必要的功能扩展和性能优化。结构清晰，易于维护，能够很好地支撑体育馆管理系统的各项业务功能。

