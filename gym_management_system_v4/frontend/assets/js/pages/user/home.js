new Vue({
    el: '#app',
    data() {
        return {
            currentPage: 'home',
            userInfo: {},
            weather: {
                city: '加载中...',
                temperature: '--',
                weather: '晴',
                humidity: '--',
                windSpeed: '--',
                updateTime: new Date()
            },
            carouselItems: [
                { image: '../../assets/images/banner1.jpg', title: '智能预约，便捷运动', description: '一键预约您心仪的场馆，开启健康生活。' },
                { image: '../../assets/images/banner2.jpg', title: '丰富场馆，多样选择', description: '篮球、羽毛球、游泳…总有适合你的运动空间。' },
                { image: '../../assets/images/banner3.jpg', title: '会员特权，尊享优惠', description: '加入会员，体验更多专属福利。' }
            ],
            facilityTypes: [],
            popularFacilities: [],
            notices: []
        }
    },
    mounted() {
        this.checkAuth();
        this.loadUserInfo();
        this.loadData();
    },
    methods: {
        // 检查登录状态
        checkAuth() {
            if (!Auth.requireUser()) {
                return;
            }
        },
        
        // 加载用户信息
        loadUserInfo() {
            this.userInfo = Auth.getUserInfo() || {};
        },
        
        // 加载页面数据
        loadData() {
            this.loadWeather();
            this.loadFacilityTypes();
            this.loadPopularFacilities();
            this.loadNotices();
        },
        
        // 加载天气信息
        loadWeather() {
            const result = MockData.getHarbinWeather();
            if (result.success) {
                this.weather = result.data;
            }
        },
        
        // 加载场馆类型
        loadFacilityTypes() {
            this.facilityTypes = MockData.facilityTypes;
        },
        
        // 加载热门场馆
        loadPopularFacilities() {
            this.popularFacilities = MockData.getFacilities().slice(0, 6);
        },
        
        // 加载公告
        loadNotices() {
            this.notices = MockData.notices;
        },
        
        // 跳转到场馆列表
        goToFacilities() {
            window.location.href = 'facilities.html';
        },
        
        // 按类型跳转到场馆列表
        goToFacilitiesByType(typeId) {
            window.location.href = `facilities.html?type=${typeId}`;
        },
        
        // 跳转到场馆详情
        goToFacilityDetail(facilityId) {
            window.location.href = `booking.html?facility_id=${facilityId}`;
        },
        
        // 获取场馆类型名称
        getFacilityTypeName(typeId) {
            const type = this.facilityTypes.find(t => t.type_id === typeId);
            return type ? type.type_name : '未知类型';
        },
        
        // 获取公告类型文本
        getNoticeTypeText(type) {
            const typeMap = {
                1: '系统公告',
                2: '营业时间',
                3: '活动通知'
            };
            return typeMap[type] || '公告';
        },
        
        // 获取公告类型颜色
        getNoticeTypeColor(type) {
            const colorMap = {
                1: 'info',
                2: 'warning',
                3: 'success'
            };
            return colorMap[type] || 'info';
        },
        
        // 获取页面标题
        getPageTitle() {
            const titleMap = {
                home: '首页',
                facilities: '场馆列表',
                profile: '个人中心',
                ai: 'AI助手'
            };
            return titleMap[this.currentPage] || '页面';
        },
        
        // 处理用户下拉菜单命令
        handleUserCommand(command) {
            switch (command) {
                case 'profile':
                    this.currentPage = 'profile';
                    break;
                case 'settings':
                    this.$message.info('设置功能开发中');
                    break;
                case 'logout':
                    this.handleLogout();
                    break;
            }
        },
        
        // 处理退出登录
        handleLogout() {
            this.$confirm('确定要退出登录吗？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                Auth.logout();
                this.$message.success('已退出登录');
                window.location.href = '../../index.html';
            }).catch(() => {});
        },
        
        // 格式化时间
        formatTime(time) {
            return dayjs(time).format('MM-DD HH:mm');
        },
        
        // 新增的页面跳转方法
        goToPage(page) {
            window.location.href = page;
        }
    }
});
