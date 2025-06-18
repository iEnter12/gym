export default {
    el: '#app',
    data() {
        return {
            userInfo: {
                username: '',
                real_name: '',
                avatar: ''
            },
            // 搜索和筛选
            searchKeyword: '',
            selectedType: null,
            sortBy: 'default',
            viewMode: 'grid',
            
            // 分页
            currentPage: 1,
            pageSize: 12,
            
            // 场馆数据
            facilities: [],
            facilityTypes: [],
            loading: false
        }
    },
    computed: {
        // 过滤后的场馆列表
        filteredFacilities() {
            let result = [...this.facilities];
            
            // 关键词搜索
            if (this.searchKeyword) {
                const keyword = this.searchKeyword.toLowerCase();
                result = result.filter(facility => 
                    facility.facility_name.toLowerCase().includes(keyword) ||
                    facility.location.toLowerCase().includes(keyword) ||
                    facility.description.toLowerCase().includes(keyword)
                );
            }
            
            // 类型筛选
            if (this.selectedType !== null) {
                result = result.filter(facility => 
                    facility.type === this.selectedType
                );
            }
            
            // 排序
            switch (this.sortBy) {
                case 'price_asc':
                    result.sort((a, b) => a.price - b.price);
                    break;
                case 'price_desc':
                    result.sort((a, b) => b.price - a.price);
                    break;
                case 'capacity_desc':
                    result.sort((a, b) => b.capacity - a.capacity);
                    break;
                default:
                    result.sort((a, b) => a.sort_order - b.sort_order);
            }
            
            return result;
        },
        
        // 分页后的场馆列表
        paginatedFacilities() {
            const start = (this.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return this.filteredFacilities.slice(start, end);
        }
    },
    mounted() {
        this.checkAuth();
        this.loadFacilityTypes();
        this.loadFacilities();
    },
    methods: {
        // 检查登录状态
        checkAuth() {
            if (!Auth.requireUser()) {
                return;
            }
            this.loadUserInfo();
        },
        
        // 加载用户信息
        loadUserInfo() {
            const userInfo = Auth.getUserInfo();
            if (userInfo) {
                this.userInfo = userInfo;
            } else {
                api.auth.getUserInfo()
                    .then(response => {
                        if (response.success) {
                            this.userInfo = response.data;
                            Auth.setUserInfo(response.data);
                        }
                    })
                    .catch(error => {
                        console.error('获取用户信息失败:', error);
                        if (error.response && error.response.status === 401) {
                            Auth.logout();
                            window.location.href = '/index.html';
                        }
                    });
            }
        },
        
        // 加载场馆类型
        loadFacilityTypes() {
            api.facilities.getTypes()
                .then(response => {
                    if (response.success) {
                        this.facilityTypes = response.data;
                    }
                })
                .catch(error => {
                    console.error('获取场馆类型失败:', error);
                    this.$message.error('获取场馆类型失败');
                });
        },
        
        // 加载场馆列表
        loadFacilities() {
            this.loading = true;
            const params = {
                page: this.currentPage,
                page_size: this.pageSize
            };
            
            // 添加类型筛选参数
            if (this.selectedType !== null) {
                params.type = this.selectedType;
            }
            
            // 添加搜索关键词
            if (this.searchKeyword) {
                params.keyword = this.searchKeyword;
            }
            
            api.facilities.getList(params)
                .then(response => {
                    if (response.success) {
                        this.facilities = response.data;
                        console.log('加载的场馆数据:', this.facilities);
                    }
                })
                .catch(error => {
                    console.error('获取场馆列表失败:', error);
                    this.$message.error('获取场馆列表失败');
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        
        // 处理搜索
        handleSearch() {
            this.currentPage = 1;
            this.loadFacilities();
        },
        
        // 选择场馆类型
        selectType(typeId) {
            this.selectedType = typeId;
            this.currentPage = 1;
            // 重新加载场馆列表，带上类型筛选参数
            this.loadFacilities();
        },
        
        // 处理排序
        handleSort() {
            this.currentPage = 1;
        },
        
        // 处理分页大小变化
        handleSizeChange(val) {
            this.pageSize = val;
            this.loadFacilities();
        },
        
        // 处理页码变化
        handleCurrentChange(val) {
            this.currentPage = val;
            this.loadFacilities();
        },
        
        // 获取场馆类型名称
        getFacilityTypeName(typeId) {
            // 如果facility对象中已经有type_name，直接返回
            if (this.facility && this.facility.type_name) {
                return this.facility.type_name;
            }
            // 否则从facilityTypes中查找
            const type = this.facilityTypes.find(t => t.type_id === typeId);
            return type ? type.type_name : '未知类型';
        },
        
        // 获取状态样式类
        getStatusClass(status) {
            const statusMap = {
                1: 'status-active',
                2: 'status-maintenance',
                3: 'status-inactive'
            };
            return statusMap[status] || 'status-unknown';
        },
        
        // 获取状态文本
        getStatusText(status) {
            const statusMap = {
                1: '可预约',
                2: '维护中',
                3: '已关闭'
            };
            return statusMap[status] || '未知状态';
        },
        
        // 跳转到预约页面
        goToBooking(facilityId) {
            window.location.href = `booking.html?facility_id=${facilityId}`;
        },
        
        // 页面跳转
        goToPage(page) {
            const pageMap = {
                home: 'home.html',
                profile: 'profile.html',
                ai: 'ai-chat.html'
            };
            if (pageMap[page]) {
                window.location.href = pageMap[page];
            }
        },
        
        // 处理用户下拉菜单命令
        handleUserCommand(command) {
            if (command === 'logout') {
                Auth.logout();
                window.location.href = '/index.html';
            }
        },
        
        // 获取场馆类型图标
        getFacilityTypeIcon(typeId) {
            const type = this.facilityTypes.find(t => t.type_id === typeId);
            return type ? type.icon : 'el-icon-question';
        }
    }
};
