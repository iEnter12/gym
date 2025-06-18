// API 接口管理
const axios = window.axios;

class API {
    constructor() {
        this.baseURL = 'http://localhost:8000/api'; // Django后端API基础路径
        this.timeout = 10000;
        
        // 配置axios默认设置
        axios.defaults.timeout = this.timeout;
        axios.defaults.headers.common['Content-Type'] = 'application/json';
        
        // 请求拦截器
        axios.interceptors.request.use(
            config => {
                const token = Auth.getToken();
                if (token) {
                    config.headers.Authorization = `Token ${token}`;
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
                console.log('API响应拦截器 - 原始响应:', response);
                console.log('API响应拦截器 - 响应数据:', response.data);
                
                // 检查是否是分页数据格式 (包含 count, next, previous, results)
                if (response.data && response.data.count !== undefined && response.data.results !== undefined) {
                    console.log('API响应拦截器 - 处理分页数据');
                    return {
                        success: true,
                        data: response.data.results,
                        pagination: {
                            count: response.data.count,
                            next: response.data.next,
                            previous: response.data.previous
                        }
                    };
                }
                
                // 处理普通API响应
                if (response.data && response.data.success !== undefined) {
                    console.log('API响应拦截器 - 处理普通API响应');
                        return response.data;
                }
                
                // 处理数组类型的响应（如场馆类型列表）
                if (Array.isArray(response.data)) {
                    console.log('API响应拦截器 - 处理数组响应');
                    return {
                        success: true,
                        data: response.data
                    };
                }
                
                // 其他情况，默认为成功
                console.log('API响应拦截器 - 处理其他响应');
                return {
                    success: true,
                    data: response.data
                };
            },
            error => {
                console.error('API响应拦截器 - 错误:', error);
                console.error('API响应拦截器 - 错误响应:', error.response);
                console.error('API响应拦截器 - 错误数据:', error.response?.data);
                
                if (error.response) {
                    const errorData = error.response.data;
                    let message = '请求失败';
                    
                    if (errorData && errorData.message) {
                        message = errorData.message;
                    } else if (errorData && errorData.errors) {
                        // 处理表单验证错误
                        const errors = errorData.errors;
                        const errorMessages = [];
                        for (const field in errors) {
                            if (Array.isArray(errors[field])) {
                                errorMessages.push(...errors[field]);
                            } else {
                                errorMessages.push(errors[field]);
                            }
                        }
                        message = errorMessages.join(', ');
                    }
                    
                    switch (error.response.status) {
                        case 401:
                            Auth.logout();
                            window.location.href = '/index.html';
                            break;
                        case 403:
                            message = '没有权限访问';
                            break;
                        case 404:
                            message = '请求的资源不存在';
                            break;
                        case 500:
                            message = '服务器内部错误';
                            break;
                    }
                    
                    // 修改错误对象，添加更详细的错误信息
                    error.response.data = {
                        ...error.response.data,
                        message: message
                    };
                } else {
                    error.response = {
                        data: {
                            message: '网络连接失败'
                        }
                    };
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
            return axios.post(`${this.baseURL}/auth/login/`, data);
        },
        
        // 用户注册
        register: (data) => {
            return axios.post(`${this.baseURL}/auth/register/`, data);
        },
        
        // 获取用户信息
        getUserInfo: () => {
            return axios.get(`${this.baseURL}/auth/user/`);
        },
        
        // 修改用户资料
        updateProfile: (data) => {
            return axios.put(`${this.baseURL}/auth/profile/`, data);
        },
        
        // 修改密码
        changePassword: (data) => {
            return axios.put(`${this.baseURL}/auth/password/`, data);
        },
        
        // 退出登录
        logout: () => {
            return axios.post(`${this.baseURL}/auth/logout/`);
        }
    };
    
    // 场馆相关API
    facilities = {
        // 获取场馆列表
        getList: (params) => {
            return axios.get(`${this.baseURL}/facilities/`, { params });
        },
        
        // 获取场馆详情
        getDetail: (id) => {
            return axios.get(`${this.baseURL}/facilities/${id}/`);
        },
        
        // 获取场馆类型
        getTypes: () => {
            return axios.get(`${this.baseURL}/facilities/types/`);
        },
        
        // 创建场馆（管理员）
        create: (data) => {
            return axios.post(`${this.baseURL}/facilities/`, data);
        },
        
        // 更新场馆（管理员）
        update: (id, data) => {
            return axios.put(`${this.baseURL}/facilities/${id}/`, data);
        },
        
        // 删除场馆（管理员）
        delete: (id) => {
            return axios.delete(`${this.baseURL}/facilities/${id}/`);
        },
        
        // 获取场馆可用时间段
        getAvailableSlots: (id, date) => {
            return axios.get(`${this.baseURL}/facilities/${id}/available-slots/`, {
                params: { date }
            });
        }
    };
    
    // 预约相关API
    bookings = {
        // 创建预约
        create: (data) => {
            return axios.post(`${this.baseURL}/bookings/create/`, data);
        },
        
        // 获取预约列表
        getList: (params) => {
            return axios.get(`${this.baseURL}/bookings/`, { params });
        },
        
        // 获取预约详情
        getDetail: (id) => {
            return axios.get(`${this.baseURL}/bookings/${id}/`);
        },
        
        // 签到预约
        checkin: (id) => {
            return axios.put(`${this.baseURL}/bookings/${id}/checkin/`);
        },
        
        // 获取用户预约列表
        getUserBookings: (params) => {
            return axios.get(`${this.baseURL}/bookings/user/`, { params });
        },
        
        // 获取场馆预约列表
        getFacilityBookings: (facilityId, params) => {
            return axios.get(`${this.baseURL}/bookings/facility/${facilityId}/`, { params });
        },
        
        // 获取用户统计数据
        getUserStats: () => {
            return axios.get(`${this.baseURL}/bookings/user/stats/`);
        },
        
        // 确定预约（用户）
        confirm: (id) => {
            return axios.put(`${this.baseURL}/bookings/${id}/confirm/`);
        },
        
        // 取消预约
        cancel: (id) => {
            return axios.delete(`${this.baseURL}/bookings/${id}/cancel/`);
        },
        
        // 获取仪表盘统计（管理员）
        getDashboard: () => {
            return axios.get(`${this.baseURL}/bookings/dashboard`);
        }
    };
    
    
    // 评价相关API
    reviews = {
        // 创建评价
        create: (data) => {
            return axios.post(`${this.baseURL}/reviews/create`, data);
        },
        
        // 获取评价列表
        getList: (params) => {
            return axios.get(`${this.baseURL}/reviews/`, { params });
        },
        
        // 获取场馆评价
        getFacilityReviews: (facilityId, params) => {
            return axios.get(`${this.baseURL}/reviews/facility/${facilityId}/`, { params });
        },
        
        // 获取用户评价
        getUserReviews: (params) => {
            return axios.get(`${this.baseURL}/reviews/user/`, { params });
        },
        
        // 回复评价（管理员）
        reply: (id, data) => {
            return axios.post(`${this.baseURL}/reviews/${id}/reply`, data);
        },
        
        // 删除评价
        delete: (id) => {
            return axios.delete(`${this.baseURL}/reviews/${id}/delete`);
        }
    };
    
    // 天气相关API
    weather = {
        // 获取哈尔滨天气
        getHarbinWeather: () => {
            return axios.get(`${this.baseURL}/weather/harbin/`);
        }
    };
    
    // AI助手相关API
    ai = {
        // 发送消息到AI助手
        sendMessage: (message) => {
            return axios.post(`${this.baseURL}/ai/chat/`, { message });
        }
    };
    
    // 系统相关API
    system = {
        // 获取系统配置
        getConfig: (key) => {
            return axios.get(`${this.baseURL}/system/config/`, { params: { key } });
        },
        
        // 更新系统配置（管理员）
        updateConfig: (key, value) => {
            return axios.put(`${this.baseURL}/system/config/`, { key, value });
        }
    };
    
    // 公告相关API
    notices = {
        // 获取公告列表
        getList: (params) => {
            return axios.get(`${this.baseURL}/notices/`, { params });
        },
        
        // 获取活跃公告
        getActive: (params) => {
            return axios.get(`${this.baseURL}/notices/active/`, { params });
        },
        
        // 获取公告详情
        getDetail: (id) => {
            return axios.get(`${this.baseURL}/notices/${id}/`);
        },
        
        // 创建公告（管理员）
        create: (data) => {
            return axios.post(`${this.baseURL}/notices/`, data);
        },
        
        // 更新公告（管理员）
        update: (id, data) => {
            return axios.put(`${this.baseURL}/notices/${id}/`, data);
        },
        
        // 删除公告（管理员）
        delete: (id) => {
            return axios.delete(`${this.baseURL}/notices/${id}/`);
        }
    };
    
    // 用户相关API
    users = {
        // 获取用户列表（管理员）
        getList: (params) => {
            return axios.get(`${this.baseURL}/users/`, { params });
        },
        
        // 获取用户详情
        getDetail: (id) => {
            return axios.get(`${this.baseURL}/users/${id}/`);
        },
        
        // 创建用户（管理员）
        create: (data) => {
            return axios.post(`${this.baseURL}/users/`, data);
        },
        
        // 更新用户（管理员）
        update: (id, data) => {
            return axios.put(`${this.baseURL}/users/${id}/`, data);
        },
        
        // 删除用户（管理员）
        delete: (id) => {
            return axios.delete(`${this.baseURL}/users/${id}/`);
        },
        
        // 获取用户统计信息
        getUserStats: () => {
            return axios.get(`${this.baseURL}/users/stats/`);
        }
    };
}

// 创建API实例
const api = new API();

// 导出为全局变量
window.API = api;

