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
                { image: '../../assets/images/carousel-basketball.jpg', title: '智能预约，便捷运动', description: '一键预约您心仪的场馆，开启健康生活。' },
                { image: '../../assets/images/carousel-badminton.jpg', title: '丰富场馆，多样选择', description: '篮球、羽毛球、游泳…总有适合你的运动空间。' },
                { image: '../../assets/images/carousel-swimming.jpg', title: '会员特权，尊享优惠', description: '加入会员，体验更多专属福利。' }
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
            // 已移除加载场馆类型
            this.loadPopularFacilities();
            // 已移除加载公告
        },
        
        // 加载天气信息
                loadWeather() {
                    api.weather.getHarbinWeather()
                        .then(response => {
                            console.log('完整响应:', response)  // 关键调试点1
                            console.log('响应数据:', response.data) // 关键调试点2

                            if (response.success) {
                                // this.weather = response.data;
                                const liveData = response.data.lives[0];
                                this.weather = {
                                    city: liveData.city || '哈尔滨',  // 使用API返回的城市名
                                    temperature: liveData.temperature || '--',  // 温度字符串
                                    weather: liveData.weather || '未知',
                                    humidity: liveData.humidity || '--',
                                    windSpeed: liveData.windpower || '--',  // 注意字段是windpower
                                    updateTime: liveData.reporttime ? 
                                    new Date(liveData.reporttime).toLocaleString() : 
                                    new Date().toLocaleString()
                                };
                            } else {
                                console.error('获取天气信息失败:', response.message);
                                this.weather = {
                                    city: '哈尔滨',
                                    temperature: '--',
                                    weather: '未知',
                                    humidity: '--',
                                    windSpeed: '--',
                                    updateTime: new Date()
                                };
                            }
                        })
                        .catch(error => {
                            console.error('获取天气信息失败:', error);
                            this.weather = {
                                city: '哈尔滨',
                                temperature: '--',
                                weather: '未知',
                                humidity: '--',
                                windSpeed: '--',
                                updateTime: new Date()
                            };
                        });
                },
        
        // 加载场馆类型
        loadFacilityTypes() {
            api.facilities.getTypes()
                .then(response => {
                    if (response.success && Array.isArray(response.data)) {
                        // 确保每个类型都有正确的图标类名
                        this.facilityTypes = response.data.map(type => {
                            // 处理图标格式
                            if (type.icon) {
                                // 如果后端返回的icon不是以el-icon开头，则添加默认前缀
                                if (!type.icon.startsWith('el-icon-')) {
                                    type.icon = 'el-icon-' + type.icon;
                                }
                            } else {
                                // 如果没有icon，设置一个默认图标
                                type.icon = 'el-icon-data-analysis';
                            }
                            return type;
                        });
                        console.log('加载场馆类型成功:', this.facilityTypes);
                    } else {
                        console.error('获取场馆类型失败:', response);
                        this.facilityTypes = [];
                    }
                })
                .catch(error => {
                    console.error('获取场馆类型失败:', error);
                    // 加载失败时，可以设置一些默认数据或显示错误提示
                });
        },
        
        // 加载热门场馆
        loadPopularFacilities() {
            api.facilities.getList({ limit: 6 })
                .then(response => {
                    if (response.success) {
                        this.popularFacilities = response.data;
                    }
                })
                .catch(error => {
                    console.error('获取热门场馆失败:', error);
                });
        },
        
        // 加载公告
        loadNotices() {
            api.notices.getActive({ limit: 5 })
                .then(response => {
                    if (response.success) {
                        this.notices = response.data;
                    }
                })
                .catch(error => {
                    console.error('获取公告失败:', error);
                });
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
