// 模拟数据管理
class MockData {
    constructor() {
        this.initData();
    }
    
    // 初始化数据
    static initData() {
        // 如果localStorage中没有数据，则初始化
        if (!localStorage.getItem('mock_users')) {
            this.resetData();
        }
    }
    
    // 重置所有模拟数据
    static resetData() {
        // 用户数据
        const users = [
            {
                account_id: 1,
                username: 'admin',
                password: '123456',
                real_name: '系统管理员',
                phone: '13800138000',
                email: 'admin@example.com',
                avatar: '',
                user_type: 2,
                status: 1,
                register_time: '2024-01-01 10:00:00',
                last_login_time: '2024-06-13 09:00:00'
            },
            {
                account_id: 2,
                username: 'user001',
                password: '123456',
                real_name: '张三',
                phone: '13800138001',
                email: 'zhangsan@example.com',
                avatar: '',
                user_type: 1,
                status: 1,
                register_time: '2024-02-01 14:30:00',
                last_login_time: '2024-06-12 18:20:00'
            },
            {
                account_id: 3,
                username: 'user002',
                password: '123456',
                real_name: '李四',
                phone: '13800138002',
                email: 'lisi@example.com',
                avatar: '',
                user_type: 1,
                status: 1,
                register_time: '2024-03-15 16:45:00',
                last_login_time: '2024-06-11 20:15:00'
            }
        ];
        
        // 场馆类型数据
        const facilityTypes = [
            {
                type_id: 1,
                type_name: '篮球场',
                icon: 'el-icon-basketball',
                description: '标准篮球场地，适合篮球运动',
                create_time: '2024-01-01 10:00:00'
            },
            {
                type_id: 2,
                type_name: '羽毛球场',
                icon: 'el-icon-badminton',
                description: '专业羽毛球场地，设施完善',
                create_time: '2024-01-01 10:00:00'
            },
            {
                type_id: 3,
                type_name: '游泳池',
                icon: 'el-icon-swimming',
                description: '标准游泳池，水质清洁',
                create_time: '2024-01-01 10:00:00'
            },
            {
                type_id: 4,
                type_name: '乒乓球室',
                icon: 'el-icon-ping-pong',
                description: '室内乒乓球场地，环境舒适',
                create_time: '2024-01-01 10:00:00'
            },
            {
                type_id: 5,
                type_name: '健身房',
                icon: 'el-icon-fitness',
                description: '现代化健身设备，专业指导',
                create_time: '2024-01-01 10:00:00'
            }
        ];
        
        // 场馆数据
        const facilities = [
            {
                facility_id: 1,
                type_id: 1,
                facility_name: '1号篮球场',
                location: '体育馆一楼东侧',
                capacity: 20,
                area: 420.00,
                image_url: '/assets/images/basketball-1.jpg',
                price: 80.00,
                description: '标准篮球场，地板为专业运动木地板，配备电子计分牌',
                status: 1,
                create_time: '2024-01-01 10:00:00'
            },
            {
                facility_id: 2,
                type_id: 1,
                facility_name: '2号篮球场',
                location: '体育馆一楼西侧',
                capacity: 20,
                area: 420.00,
                image_url: '/assets/images/basketball-2.jpg',
                price: 80.00,
                description: '标准篮球场，设施完善，适合比赛和训练',
                status: 1,
                create_time: '2024-01-01 10:00:00'
            },
            {
                facility_id: 3,
                type_id: 2,
                facility_name: '1号羽毛球场',
                location: '体育馆二楼A区',
                capacity: 4,
                area: 81.00,
                image_url: '/assets/images/badminton-1.jpg',
                price: 60.00,
                description: '专业羽毛球场地，采用进口地胶，灯光充足',
                status: 1,
                create_time: '2024-01-01 10:00:00'
            },
            {
                facility_id: 4,
                type_id: 2,
                facility_name: '2号羽毛球场',
                location: '体育馆二楼B区',
                capacity: 4,
                area: 81.00,
                image_url: '/assets/images/badminton-2.jpg',
                price: 60.00,
                description: '标准羽毛球场，通风良好，环境舒适',
                status: 1,
                create_time: '2024-01-01 10:00:00'
            },
            {
                facility_id: 5,
                type_id: 3,
                facility_name: '标准游泳池',
                location: '游泳馆',
                capacity: 50,
                area: 1250.00,
                image_url: '/assets/images/swimming-pool.jpg',
                price: 40.00,
                description: '50米标准游泳池，8条泳道，水质清洁，配备救生员',
                status: 1,
                create_time: '2024-01-01 10:00:00'
            },
            {
                facility_id: 6,
                type_id: 4,
                facility_name: '乒乓球室A',
                location: '体育馆三楼',
                capacity: 8,
                area: 200.00,
                image_url: '/assets/images/pingpong-room.jpg',
                price: 30.00,
                description: '室内乒乓球场地，配备专业球台和照明',
                status: 1,
                create_time: '2024-01-01 10:00:00'
            }
        ];
        
        // 会员套餐数据 - 已删除
        const membershipPackages = [];
        
        // 公告数据
        const notices = [
            {
                notice_id: 1,
                title: '营业时间调整通知',
                content: '本体育馆营业时间为每日6:00-22:00，请合理安排运动时间。',
                notice_type: 2,
                start_time: '2024-06-01 00:00:00',
                end_time: '2024-12-31 23:59:59',
                is_published: 1,
                create_time: '2024-06-01 10:00:00'
            },
            {
                notice_id: 2,
                title: '端午节活动优惠',
                content: '端午节期间（6月10日-12日）所有场馆8折优惠，欢迎预约！',
                notice_type: 3,
                start_time: '2024-06-08 00:00:00',
                end_time: '2024-06-12 23:59:59',
                is_published: 1,
                create_time: '2024-06-08 09:00:00'
            },
            {
                notice_id: 3,
                title: '设施维护通知',
                content: '2号篮球场将于6月15日进行设施维护，当日暂停开放，给您带来不便敬请谅解。',
                notice_type: 1,
                start_time: '2024-06-13 00:00:00',
                end_time: '2024-06-15 23:59:59',
                is_published: 1,
                create_time: '2024-06-13 08:00:00'
            }
        ];
        
        // 保存到localStorage
        localStorage.setItem('mock_users', JSON.stringify(users));
        localStorage.setItem('mock_facility_types', JSON.stringify(facilityTypes));
        localStorage.setItem('mock_facilities', JSON.stringify(facilities));
        // 会员相关数据已下线
        localStorage.setItem('mock_membership_packages', JSON.stringify([]));
        localStorage.setItem('mock_notices', JSON.stringify(notices));
        localStorage.setItem('mock_bookings', JSON.stringify([]));
        // 订单相关数据已删除
        // 会员相关数据已下线
        localStorage.setItem('mock_memberships', JSON.stringify([]));
        localStorage.setItem('mock_reviews', JSON.stringify([]));
    }
    
    // 获取数据
    static getData(key) {
        const data = localStorage.getItem(`mock_${key}`);
        return data ? JSON.parse(data) : [];
    }
    
    // 保存数据
    static saveData(key, data) {
        localStorage.setItem(`mock_${key}`, JSON.stringify(data));
    }
    
    // 生成ID
    static generateId(key) {
        const data = this.getData(key);
        return data.length > 0 ? Math.max(...data.map(item => item[`${key.slice(0, -1)}_id`] || item.id)) + 1 : 1;
    }
    
    // 用户登录
    static login(loginData) {
        const users = this.getData('users');
        const user = users.find(u => 
            (u.username === loginData.username || u.phone === loginData.username) &&
            u.password === loginData.password &&
            u.user_type === loginData.userType
        );
        
        if (user) {
            if (user.status !== 1) {
                return { success: false, message: '账号已被禁用' };
            }
            
            // 更新最后登录时间
            user.last_login_time = new Date().toISOString().slice(0, 19).replace('T', ' ');
            this.saveData('users', users);
            
            return {
                success: true,
                data: {
                    token: 'mock_token_' + user.account_id + '_' + Date.now(),
                    user: user
                }
            };
        } else {
            return { success: false, message: '用户名或密码错误' };
        }
    }
    
    // 用户注册
    static register(registerData) {
        const users = this.getData('users');
        
        // 检查用户名是否已存在
        if (users.find(u => u.username === registerData.username)) {
            return { success: false, message: '用户名已存在' };
        }
        
        // 检查手机号是否已存在
        if (users.find(u => u.phone === registerData.phone)) {
            return { success: false, message: '手机号已被注册' };
        }
        
        // 创建新用户
        const newUser = {
            account_id: this.generateId('users'),
            username: registerData.username,
            password: registerData.password,
            real_name: registerData.realName,
            phone: registerData.phone,
            email: registerData.email || '',
            avatar: '',
            user_type: 1, // 普通用户
            status: 1, // 正常
            register_time: new Date().toISOString().slice(0, 19).replace('T', ' '),
            last_login_time: null,
            create_time: new Date().toISOString().slice(0, 19).replace('T', ' '),
            update_time: new Date().toISOString().slice(0, 19).replace('T', ' ')
        };
        
        users.push(newUser);
        this.saveData('users', users);
        
        return { success: true, message: '注册成功' };
    }
    
    // 获取公告列表
    static get notices() {
        return this.getData('notices').filter(notice => notice.is_published === 1);
    }
    
    // 获取场馆类型
    static get facilityTypes() {
        return this.getData('facility_types');
    }
    
    // 获取场馆列表
    static getFacilities(params = {}) {
        let facilities = this.getData('facilities');
        
        // 按类型筛选
        if (params.type_id) {
            facilities = facilities.filter(f => f.type_id == params.type_id);
        }
        
        // 按状态筛选
        if (params.status) {
            facilities = facilities.filter(f => f.status == params.status);
        }
        
        // 搜索
        if (params.keyword) {
            facilities = facilities.filter(f => 
                f.facility_name.includes(params.keyword) ||
                f.description.includes(params.keyword)
            );
        }
        
        return facilities;
    }
    
    // 获取场馆详情
    static getFacilityDetail(id) {
        const facilities = this.getData('facilities');
        return facilities.find(f => f.facility_id == id);
    }
    
    // 获取会员套餐 - 已下线
    static get membershipPackages() {
        return [];
    }
    
    // 获取哈尔滨天气（模拟）
    static getHarbinWeather() {
        const weathers = [
            { temp: 18, weather: '晴', icon: 'sunny' },
            { temp: 15, weather: '多云', icon: 'cloudy' },
            { temp: 12, weather: '小雨', icon: 'rainy' },
            { temp: 20, weather: '晴', icon: 'sunny' }
        ];
        
        const today = weathers[Math.floor(Math.random() * weathers.length)];
        
        return {
            success: true,
            data: {
                city: '哈尔滨',
                temperature: today.temp,
                weather: today.weather,
                icon: today.icon,
                humidity: Math.floor(Math.random() * 40) + 40,
                windSpeed: Math.floor(Math.random() * 10) + 5,
                updateTime: new Date().toISOString().slice(0, 19).replace('T', ' ')
            }
        };
    }
    
    // 创建预约
    static createBooking(bookingData) {
        const bookings = this.getData('bookings');
        
        // 检查时间冲突
        const conflict = bookings.find(b => 
            b.facility_id == bookingData.facility_id &&
            b.booking_date === bookingData.booking_date &&
            b.status !== 3 && // 非已取消
            (
                (bookingData.start_time >= b.start_time && bookingData.start_time < b.end_time) ||
                (bookingData.end_time > b.start_time && bookingData.end_time <= b.end_time) ||
                (bookingData.start_time <= b.start_time && bookingData.end_time >= b.end_time)
            )
        );
        
        if (conflict) {
            return { success: false, message: '该时间段已被预约' };
        }
        
        const newBooking = {
            booking_id: this.generateId('bookings'),
            account_id: bookingData.account_id,
            facility_id: bookingData.facility_id,
            booking_date: bookingData.booking_date,
            start_time: bookingData.start_time,
            end_time: bookingData.end_time,
            person_count: bookingData.person_count || 1,
            status: 0, // 未开始
            remark: bookingData.remark || '',
            is_member_used: bookingData.is_member_used || 0,
            create_time: new Date().toISOString().slice(0, 19).replace('T', ' '),
            update_time: new Date().toISOString().slice(0, 19).replace('T', ' ')
        };
        
        bookings.push(newBooking);
        this.saveData('bookings', bookings);
        
        return { success: true, data: newBooking };
    }
    
    // 获取用户预约
    static getUserBookings(accountId, params = {}) {
        let bookings = this.getData('bookings').filter(b => b.account_id == accountId);
        
        // 按状态筛选
        if (params.status !== undefined) {
            bookings = bookings.filter(b => b.status == params.status);
        }
        
        // 按日期筛选
        if (params.date) {
            bookings = bookings.filter(b => b.booking_date === params.date);
        }
        
        return bookings.sort((a, b) => new Date(b.create_time) - new Date(a.create_time));
    }
    
    // 获取用户统计数据
    static getUserStats(accountId) {
        const bookings = this.getData('mock_bookings') || [];
        const userBookings = bookings.filter(booking => booking.account_id === accountId);
        
        return {
            totalBookings: userBookings.length,
            completedBookings: userBookings.filter(b => b.status === 'completed').length,
            cancelledBookings: userBookings.filter(b => b.status === 'cancelled').length,
            pendingBookings: userBookings.filter(b => b.status === 'pending').length
        };
    }
    
    // AI聊天模拟
    static aiChat(message) {
        const responses = [
            '关于体育运动，我建议您根据个人兴趣和身体状况选择合适的项目。',
            '篮球是一项很好的有氧运动，可以提高心肺功能和协调性。',
            '游泳是全身性运动，对关节冲击小，适合各个年龄段的人群。',
            '羽毛球运动强度适中，是很好的休闲健身选择。',
            '建议运动前做好热身，运动后进行拉伸，避免运动损伤。',
            '保持规律的运动习惯比偶尔的高强度运动更有益健康。'
        ];
        
        const response = responses[Math.floor(Math.random() * responses.length)];
        
        return {
            success: true,
            data: {
                message: response,
                timestamp: new Date().toISOString().slice(0, 19).replace('T', ' ')
            }
        };
    }
}

// 初始化模拟数据
MockData.initData();

