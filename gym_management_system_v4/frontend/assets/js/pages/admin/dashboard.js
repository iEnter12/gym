new Vue({
    el: '#app',
    data() {
        return {
            // 侧边栏
            sidebarCollapsed: false,
            activeMenu: 'dashboard',
            
            // 管理员信息
            adminInfo: {
                username: '',
                avatar: ''
            },
            
            // 统计数据
            stats: {
                facilities: {
                    total: 0,
                    available: 0
                },
                bookings: {
                    today: 0,
                    week: 0
                }
            },
            
            // 预约状态数据
            bookingStatusData: [],
            
            // 最近预约记录
            recentBookings: [],
            loading: false
        };
    },
    created() {
        this.loadAdminInfo();
        this.loadDashboardData();
    },
    methods: {
        // 加载管理员信息
        loadAdminInfo() {
            const adminInfo = Auth.getUserInfo();
            if (adminInfo) {
                this.adminInfo = adminInfo;
            }
        },
        
        // 加载仪表盘数据
        loadDashboardData() {
            this.loading = true;
            
            // 加载场馆统计
            api.facilities.getList()
                .then(response => {
                    const facilities = response.results || response.data?.results || response.data || [];
                    this.stats.facilities.total = facilities.length;
                    this.stats.facilities.available = facilities.filter(f => f.status === 1).length;
                })
                .catch(error => {
                    console.error('获取场馆统计失败:', error);
                });
            
            // 加载预约统计
            const today = dayjs().format('YYYY-MM-DD');
            const weekStart = dayjs().startOf('week').format('YYYY-MM-DD');
            const weekEnd = dayjs().endOf('week').format('YYYY-MM-DD');
            
            Promise.all([
                // 获取今日预约
                api.bookings.getList({ 
                    page: 1, 
                    page_size: 100,
                    date: today
                }),
                // 获取本周预约
                api.bookings.getList({ 
                    page: 1, 
                    page_size: 100,
                    date_start: weekStart,
                    date_end: weekEnd
                })
            ]).then(([todayResponse, weekResponse]) => {
                const todayBookings = todayResponse.results || todayResponse.data?.results || todayResponse.data || [];
                const weekBookings = weekResponse.results || weekResponse.data?.results || weekResponse.data || [];
                
                this.stats.bookings.today = todayBookings.length;
                this.stats.bookings.week = weekBookings.length;
                
                // 使用本周预约数据计算状态分布
                this.calculateBookingStatus(weekBookings);
                
                this.loading = false;
            }).catch(error => {
                console.error('获取预约统计失败:', error);
                this.loading = false;
            });
        },
        
        // 计算预约状态分布
        calculateBookingStatus(bookings) {
            const statusMap = {
                0: { status: 0, statusText: '未开始', count: 0 },
                1: { status: 1, statusText: '进行中', count: 0 },
                2: { status: 2, statusText: '已完成', count: 0 },
                3: { status: 3, statusText: '已取消', count: 0 },
                4: { status: 4, statusText: '已过期', count: 0 }
            };
            
            // 统计各状态数量
            bookings.forEach(booking => {
                if (statusMap[booking.status]) {
                    statusMap[booking.status].count++;
                }
            });
            
            // 计算总数和百分比
            const total = bookings.length;
            this.bookingStatusData = Object.values(statusMap).map(item => ({
                ...item,
                percentage: total > 0 ? Math.round((item.count / total) * 100) : 0
            }));
        },
        
        // 获取状态标签类型
        getStatusTagType(status) {
            const typeMap = {
                0: 'info',    // 未开始
                1: 'warning', // 进行中
                2: 'success', // 已完成
                3: 'danger',  // 已取消
                4: 'info'     // 已过期
            };
            return typeMap[status] || 'info';
        },
        
        // 获取状态文本
        getStatusText(status) {
            const statusMap = {
                0: '未开始',
                1: '进行中',
                2: '已完成',
                3: '已取消',
                4: '已过期'
            };
            return statusMap[status] || '未知';
        },
        
        // 获取状态颜色
        getStatusColor(status) {
            const colorMap = {
                0: '#909399', // 未开始
                1: '#E6A23C', // 进行中
                2: '#67C23A', // 已完成
                3: '#F56C6C', // 已取消
                4: '#909399'  // 已过期
            };
            return colorMap[status] || '#909399';
        },
        
        // 格式化日期
        formatDate(date) {
            return dayjs(date).format('YYYY-MM-DD');
        },
        
        // 处理用户下拉菜单命令
        handleUserCommand(command) {
            if (command === 'logout') {
                Auth.logout();
                window.location.href = '/index.html';
            }
        },
        
        // 页面跳转
        goToPage(page) {
            this.activeMenu = page;
            const pageMap = {
                dashboard: 'dashboard.html',
                facilities: 'facilities.html',
                bookings: 'bookings.html'
            };
            if (pageMap[page] && page !== 'dashboard') {
                window.location.href = pageMap[page];
            }
        }
    }
}); 