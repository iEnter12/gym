// API 接口管理
class API {
    constructor() {
        this.baseURL = '/api'; // 后端API基础路径
        this.timeout = 10000;
        
        // 配置axios默认设置
        axios.defaults.timeout = this.timeout;
        axios.defaults.headers.common['Content-Type'] = 'application/json';
        
        // 请求拦截器
        axios.interceptors.request.use(
            config => {
                const token = Auth.getToken();
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                }
                return config;
            },
            error => {
                return Promise.reject(error);
            }
        );
        
        // 响应拦截器
        axios.interceptors.response.use(
            response => {
                return response.data;
            },
            error => {
                if (error.response) {
                    switch (error.response.status) {
                        case 401:
                            Auth.logout();
                            window.location.href = '/index.html';
                            break;
                        case 403:
                            this.showError('没有权限访问');
                            break;
                        case 404:
                            this.showError('请求的资源不存在');
                            break;
                        case 500:
                            this.showError('服务器内部错误');
                            break;
                        default:
                            this.showError(error.response.data.message || '请求失败');
                    }
                } else {
                    this.showError('网络连接失败');
                }
                return Promise.reject(error);
            }
        );
    }
    
    // 显示错误信息
    showError(message) {
        if (typeof this.$message !== 'undefined') {
            this.$message.error(message);
        } else {
            alert(message);
        }
    }
    
    // 用户认证相关API
    auth = {
        // 用户登录
        login: (data) => {
            return axios.post(`${this.baseURL}/auth/login`, data);
        },
        
        // 用户注册
        register: (data) => {
            return axios.post(`${this.baseURL}/auth/register`, data);
        },
        
        // 获取用户信息
        getUserInfo: () => {
            return axios.get(`${this.baseURL}/auth/user`);
        },
        
        // 修改密码
        changePassword: (data) => {
            return axios.put(`${this.baseURL}/auth/password`, data);
        },
        
        // 退出登录
        logout: () => {
            return axios.post(`${this.baseURL}/auth/logout`);
        }
    };
    
    // 场馆相关API
    facilities = {
        // 获取场馆列表
        getList: (params) => {
            return axios.get(`${this.baseURL}/facilities`, { params });
        },
        
        // 获取场馆详情
        getDetail: (id) => {
            return axios.get(`${this.baseURL}/facilities/${id}`);
        },
        
        // 获取场馆类型
        getTypes: () => {
            return axios.get(`${this.baseURL}/facility-types`);
        },
        
        // 创建场馆（管理员）
        create: (data) => {
            return axios.post(`${this.baseURL}/facilities`, data);
        },
        
        // 更新场馆（管理员）
        update: (id, data) => {
            return axios.put(`${this.baseURL}/facilities/${id}`, data);
        },
        
        // 删除场馆（管理员）
        delete: (id) => {
            return axios.delete(`${this.baseURL}/facilities/${id}`);
        },
        
        // 获取场馆可用时间段
        getAvailableSlots: (id, date) => {
            return axios.get(`${this.baseURL}/facilities/${id}/available-slots`, {
                params: { date }
            });
        }
    };
    
    // 预约相关API
    bookings = {
        // 创建预约
        create: (data) => {
            return axios.post(`${this.baseURL}/bookings`, data);
        },
        
        // 获取用户预约列表
        getUserBookings: (params) => {
            return axios.get(`${this.baseURL}/bookings/user`, { params });
        },
        
        // 获取所有预约（管理员）
        getAll: (params) => {
            return axios.get(`${this.baseURL}/bookings`, { params });
        },
        
        // 取消预约
        cancel: (id) => {
            return axios.put(`${this.baseURL}/bookings/${id}/cancel`);
        },
        
        // 确认预约（管理员）
        confirm: (id) => {
            return axios.put(`${this.baseURL}/bookings/${id}/confirm`);
        },
        
        // 完成预约
        complete: (id) => {
            return axios.put(`${this.baseURL}/bookings/${id}/complete`);
        }
    };
    
    // 订单相关API
    orders = {
        // 创建订单
        create: (data) => {
            return axios.post(`${this.baseURL}/orders`, data);
        },
        
        // 获取用户订单
        getUserOrders: (params) => {
            return axios.get(`${this.baseURL}/orders/user`, { params });
        },
        
        // 获取所有订单（管理员）
        getAll: (params) => {
            return axios.get(`${this.baseURL}/orders`, { params });
        },
        
        // 支付订单
        pay: (id, data) => {
            return axios.post(`${this.baseURL}/orders/${id}/pay`, data);
        },
        
        // 退款订单
        refund: (id) => {
            return axios.post(`${this.baseURL}/orders/${id}/refund`);
        }
    };
    
    // 会员相关API（已下线）
    memberships = {
        // 获取会员套餐（已下线）
        getPackages: () => {
            console.log('会员功能已下线');
            return Promise.resolve({ data: [] });
        },
        
        // 购买会员（已下线）
        purchase: (data) => {
            console.log('会员功能已下线');
            return Promise.reject(new Error('会员功能已下线'));
        },
        
        // 获取用户会员状态（已下线）
        getUserMembership: () => {
            console.log('会员功能已下线');
            return Promise.resolve({ data: null });
        },
        
        // 获取所有会员（管理员）（已下线）
        getAll: (params) => {
            console.log('会员功能已下线');
            return Promise.resolve({ data: { list: [], total: 0 } });
        },
        
        // 创建会员套餐（管理员）（已下线）
        createPackage: (data) => {
            console.log('会员功能已下线');
            return Promise.reject(new Error('会员功能已下线'));
        },
        
        // 更新会员套餐（管理员）（已下线）
        updatePackage: (id, data) => {
            console.log('会员功能已下线');
            return Promise.reject(new Error('会员功能已下线'));
        }
    };
    
    // 评价相关API
    reviews = {
        // 创建评价
        create: (data) => {
            return axios.post(`${this.baseURL}/reviews`, data);
        },
        
        // 获取场馆评价
        getFacilityReviews: (facilityId, params) => {
            return axios.get(`${this.baseURL}/reviews/facility/${facilityId}`, { params });
        },
        
        // 获取用户评价
        getUserReviews: (params) => {
            return axios.get(`${this.baseURL}/reviews/user`, { params });
        },
        
        // 删除评价
        delete: (id) => {
            return axios.delete(`${this.baseURL}/reviews/${id}`);
        }
    };
    
    // 公告相关API
    notices = {
        // 获取公告列表
        getList: (params) => {
            return axios.get(`${this.baseURL}/notices`, { params });
        },
        
        // 创建公告（管理员）
        create: (data) => {
            return axios.post(`${this.baseURL}/notices`, data);
        },
        
        // 更新公告（管理员）
        update: (id, data) => {
            return axios.put(`${this.baseURL}/notices/${id}`, data);
        },
        
        // 删除公告（管理员）
        delete: (id) => {
            return axios.delete(`${this.baseURL}/notices/${id}`);
        }
    };
    
    // 统计相关API（管理员）
    statistics = {
        // 获取仪表盘数据
        getDashboard: () => {
            return axios.get(`${this.baseURL}/statistics/dashboard`);
        },
        
        // 获取收入统计
        getRevenue: (params) => {
            return axios.get(`${this.baseURL}/statistics/revenue`, { params });
        },
        
        // 获取场馆使用率
        getFacilityUsage: (params) => {
            return axios.get(`${this.baseURL}/statistics/facility-usage`, { params });
        },
        
        // 获取用户增长统计
        getUserGrowth: (params) => {
            return axios.get(`${this.baseURL}/statistics/user-growth`, { params });
        }
    };
    
    // 用户管理API（管理员）
    users = {
        // 获取用户列表
        getList: (params) => {
            return axios.get(`${this.baseURL}/users`, { params });
        },
        
        // 获取用户详情
        getDetail: (id) => {
            return axios.get(`${this.baseURL}/users/${id}`);
        },
        
        // 更新用户状态
        updateStatus: (id, status) => {
            return axios.put(`${this.baseURL}/users/${id}/status`, { status });
        },
        
        // 重置用户密码
        resetPassword: (id) => {
            return axios.put(`${this.baseURL}/users/${id}/reset-password`);
        }
    };
    
    // 天气API
    weather = {
        // 获取哈尔滨天气
        getHarbinWeather: () => {
            return axios.get(`${this.baseURL}/weather/harbin`);
        }
    };
    
    // AI聊天API
    ai = {
        // 发送消息
        chat: (data) => {
            return axios.post(`${this.baseURL}/ai/chat`, data);
        },
        
        // 获取聊天历史
        getChatHistory: (params) => {
            return axios.get(`${this.baseURL}/ai/chat-history`, { params });
        }
    };
}

// 创建API实例
const api = new API();

