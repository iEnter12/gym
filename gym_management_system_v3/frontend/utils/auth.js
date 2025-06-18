// 认证管理工具类
class Auth {
    constructor() {
        this.tokenKey = 'sports_venue_token';
        this.userInfoKey = 'sports_venue_user';
        this.rememberKey = 'sports_venue_remember';
    }
    
    // 设置token
    static setToken(token) {
        localStorage.setItem('sports_venue_token', token);
    }
    
    // 获取token
    static getToken() {
        return localStorage.getItem('sports_venue_token');
    }
    
    // 移除token
    static removeToken() {
        localStorage.removeItem('sports_venue_token');
    }
    
    // 设置用户信息
    static setUserInfo(userInfo) {
        localStorage.setItem('sports_venue_user', JSON.stringify(userInfo));
    }
    
    // 获取用户信息
    static getUserInfo() {
        const userInfo = localStorage.getItem('sports_venue_user');
        return userInfo ? JSON.parse(userInfo) : null;
    }
    
    // 移除用户信息
    static removeUserInfo() {
        localStorage.removeItem('sports_venue_user');
    }
    
    // 检查是否已登录
    static isLoggedIn() {
        return !!this.getToken();
    }
    
    // 检查是否为管理员
    static isAdmin() {
        const userInfo = this.getUserInfo();
        return userInfo && userInfo.user_type === 2;
    }
    
    // 检查是否为普通用户
    static isUser() {
        const userInfo = this.getUserInfo();
        return userInfo && userInfo.user_type === 1;
    }
    
    // 获取用户ID
    static getUserId() {
        const userInfo = this.getUserInfo();
        return userInfo ? userInfo.account_id : null;
    }
    
    // 获取用户名
    static getUsername() {
        const userInfo = this.getUserInfo();
        return userInfo ? userInfo.username : null;
    }
    
    // 获取真实姓名
    static getRealName() {
        const userInfo = this.getUserInfo();
        return userInfo ? userInfo.real_name : null;
    }
    
    // 获取用户头像
    static getAvatar() {
        const userInfo = this.getUserInfo();
        return userInfo ? userInfo.avatar : null;
    }
    
    // 记住账号密码
    static rememberAccount(username, password) {
        const rememberData = {
            username,
            password,
            timestamp: Date.now()
        };
        localStorage.setItem('sports_venue_remember', JSON.stringify(rememberData));
    }
    
    // 获取记住的账号
    static getRememberedAccount() {
        const rememberData = localStorage.getItem('sports_venue_remember');
        if (rememberData) {
            const data = JSON.parse(rememberData);
            // 检查是否过期（30天）
            const expireTime = 30 * 24 * 60 * 60 * 1000;
            if (Date.now() - data.timestamp < expireTime) {
                return {
                    username: data.username,
                    password: data.password
                };
            } else {
                this.clearRememberedAccount();
            }
        }
        return null;
    }
    
    // 清除记住的账号
    static clearRememberedAccount() {
        localStorage.removeItem('sports_venue_remember');
    }
    
    // 退出登录
    static logout() {
        this.removeToken();
        this.removeUserInfo();
        // 不清除记住的账号，用户可能还想使用
    }
    
    // 完全清除所有数据
    static clearAll() {
        this.removeToken();
        this.removeUserInfo();
        this.clearRememberedAccount();
    }
    
    // 检查权限
    static hasPermission(permission) {
        const userInfo = this.getUserInfo();
        if (!userInfo) return false;
        
        // 管理员拥有所有权限
        if (userInfo.user_type === 2) return true;
        
        // 普通用户权限检查
        const userPermissions = [
            'view_facilities',
            'create_booking',
            'view_own_bookings',
            'cancel_own_booking',
            'create_review',
            'view_own_reviews',
            'update_own_profile',
            'ai_chat'
        ];
        
        return userPermissions.includes(permission);
    }
    
    // 检查管理员权限
    static hasAdminPermission(permission) {
        if (!this.isAdmin()) return false;
        
        const adminPermissions = [
            'manage_facilities',
            'manage_bookings',
            'manage_users',
            'manage_reviews',
            'manage_notices',
            'view_statistics',
            'export_data'
        ];
        
        return adminPermissions.includes(permission);
    }
    
    // 路由守卫 - 检查登录状态
    static requireAuth() {
        if (!this.isLoggedIn()) {
            window.location.href = '/index.html';
            return false;
        }
        return true;
    }
    
    // 路由守卫 - 检查管理员权限
    static requireAdmin() {
        if (!this.requireAuth()) return false;
        
        if (!this.isAdmin()) {
            alert('您没有管理员权限');
            window.location.href = '/pages/user/home.html';
            return false;
        }
        return true;
    }
    
    // 路由守卫 - 检查普通用户权限
    static requireUser() {
        if (!this.requireAuth()) return false;
        
        if (!this.isUser()) {
            alert('此页面仅限普通用户访问');
            window.location.href = '/pages/admin/dashboard.html';
            return false;
        }
        return true;
    }
    
    // 自动跳转到对应首页
    static redirectToHome() {
        if (this.isAdmin()) {
            window.location.href = '/pages/admin/dashboard.html';
        } else if (this.isUser()) {
            window.location.href = '/pages/user/home.html';
        } else {
            window.location.href = '/index.html';
        }
    }
    
    // 格式化用户显示名称
    static getDisplayName() {
        const userInfo = this.getUserInfo();
        if (!userInfo) return '未登录';
        
        return userInfo.real_name || userInfo.username || '用户';
    }
    
    // 获取用户状态文本
    static getUserStatusText() {
        const userInfo = this.getUserInfo();
        if (!userInfo) return '未登录';
        
        const statusMap = {
            1: '正常',
            2: '禁用'
        };
        
        return statusMap[userInfo.status] || '未知';
    }
    
    // 获取用户类型文本
    static getUserTypeText() {
        const userInfo = this.getUserInfo();
        if (!userInfo) return '未登录';
        
        const typeMap = {
            1: '普通用户',
            2: '管理员'
        };
        
        return typeMap[userInfo.user_type] || '未知';
    }
    
    // 更新用户信息
    static updateUserInfo(newUserInfo) {
        const currentUserInfo = this.getUserInfo();
        if (currentUserInfo) {
            const updatedUserInfo = { ...currentUserInfo, ...newUserInfo };
            this.setUserInfo(updatedUserInfo);
        }
    }
    
    // 检查token是否即将过期
    static isTokenExpiringSoon() {
        // Django Token认证不会自动过期，除非手动删除
        return false;
    }
    
    // 处理登录成功
    static handleLoginSuccess(response) {
        if (response.success && response.data) {
            // 保存token和用户信息
            this.setToken(response.data.token);
            this.setUserInfo(response.data.user);
            return true;
        }
        return false;
    }
    
    // 处理登录失败
    static handleLoginError(error) {
        console.error('登录失败:', error);
        this.logout();
    }
    
    // 验证用户信息完整性
    static validateUserInfo() {
        const userInfo = this.getUserInfo();
        if (!userInfo) return false;
        
        // 检查必要字段
        const requiredFields = ['account_id', 'username', 'user_type'];
        return requiredFields.every(field => userInfo[field] !== undefined);
    }
    
    // 获取用户权限列表
    static getUserPermissions() {
        const userInfo = this.getUserInfo();
        if (!userInfo) return [];
        
        if (userInfo.user_type === 2) {
            // 管理员权限
            return [
                'manage_facilities',
                'manage_bookings', 
                'manage_users',
                'manage_reviews',
                'manage_notices',
                'view_statistics',
                'export_data'
            ];
        } else {
            // 普通用户权限
            return [
                'view_facilities',
                'create_booking',
                'view_own_bookings',
                'cancel_own_booking',
                'create_review',
                'view_own_reviews',
                'update_own_profile',
                'ai_chat'
            ];
        }
    }
}

