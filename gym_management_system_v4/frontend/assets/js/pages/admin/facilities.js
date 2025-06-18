new Vue({
    el: '#app',
    data() {
        return {
            adminInfo: {
                username: '',
                avatar: '',
                role: ''
            },
            sidebarCollapsed: false,
            activeMenu: 'facilities',
            loading: false,
            saving: false,
            searchKeyword: '',
            statusFilter: '',
            currentPage: 1,
            pageSize: 10,
            totalFacilities: 0,
            facilities: [],
            filteredFacilities: [],
            facilityStats: {
                total: 0,
                active: 0,
                maintenance: 0,
                inactive: 0
            },
            dialogVisible: false,
            viewDialogVisible: false,
            dialogMode: 'add',
            selectedFacility: null,
            facilityTypes: [],
            facilityForm: {
                facility_name: '',
                type: '',
                location: '',
                capacity: '',
                area: '',
                price: '',
                description: '',
                status: 1,
                opening_hours: '06:00-22:00',
                advance_booking_days: 7,
                min_booking_duration: 1,
                max_booking_duration: 4,
                sort_order: 0,
                image_url: ''
            },
            facilityFormRules: {
                facility_name: [
                    { required: true, message: '请输入场馆名称', trigger: 'blur' }
                ],
                type: [
                    { required: true, message: '请选择场馆类型', trigger: 'change' }
                ],
                location: [
                    { required: true, message: '请输入场馆位置', trigger: 'blur' }
                ],
                capacity: [
                    { required: true, message: '请输入容纳人数', trigger: 'blur' }
                ],
                area: [
                    { required: true, message: '请输入场地面积', trigger: 'blur' }
                ],
                price: [
                    { required: true, message: '请输入场地价格', trigger: 'blur' }
                ]
            },
            statusOptions: [
                { value: 1, label: '可用', type: 'success' },
                { value: 2, label: '维护中', type: 'warning' },
                { value: 3, label: '已关闭', type: 'danger' }
            ]
        };
    },
    computed: {
        queryParams() {
            const params = {
                page: this.currentPage,
                page_size: this.pageSize
            };
            
            if (this.searchKeyword) {
                params.keyword = this.searchKeyword;
            }
            
            if (this.statusFilter) {
                params.status = this.statusFilter;
            }
            
            return params;
        }
    },
    mounted() {
        this.checkAuth();
        this.loadFacilityTypes();
    },
    methods: {
        // 检查登录状态
        checkAuth() {
            if (!Auth.isLoggedIn()) {
                window.location.href = '/index.html';
                return;
            }
            this.loadAdminInfo();
            this.loadFacilities();
        },
        
        // 加载管理员信息
        loadAdminInfo() {
            api.auth.getUserInfo()
                .then(response => {
                    if (response.success) {
                        this.adminInfo = response.data;
                    }
                })
                .catch(error => {
                    console.error('获取管理员信息失败:', error);
                    // 如果获取用户信息失败，可能是token过期，跳转到登录页
                    if (error.response && error.response.status === 401) {
                        Auth.logout();
                        window.location.href = '/index.html';
                    }
                });
        },
        
        // 加载场馆列表
        loadFacilities() {
            this.loading = true;
            console.log('开始加载场馆列表，参数:', this.queryParams);
            
            api.facilities.getList(this.queryParams)
                .then(response => {
                    console.log('场馆列表API响应:', response);
                    // 直接适配 DRF 分页格式
                    this.facilities = response.results || response.data?.results || response.data || [];
                    this.totalFacilities = response.count || this.facilities.length;
                    this.updateFacilityStats();
                    this.loading = false;
                })
                .catch(error => {
                    console.error('获取场馆列表失败:', error);
                    console.error('错误详情:', error.response || error);
                    this.loading = false;
                });
        },
        
        // 更新场馆统计信息
        updateFacilityStats() {
            this.facilityStats = {
                total: this.facilities.length,
                active: this.facilities.filter(f => f.status === 1).length,
                maintenance: this.facilities.filter(f => f.status === 2).length,
                inactive: this.facilities.filter(f => f.status === 3).length
            };
        },
        
        // 获取状态类型
        getStatusType(status) {
            const option = this.statusOptions.find(opt => opt.value === status);
            return option ? option.type : 'info';
        },
        
        // 获取状态文本
        getStatusText(status) {
            const option = this.statusOptions.find(opt => opt.value === status);
            return option ? option.label : '未知';
        },
        
        // 获取状态标签类型
        getStatusTagType(status) {
            const typeMap = {
                1: 'success',
                2: 'warning',
                3: 'danger'
            };
            return typeMap[status] || 'info';
        },
        
        // 获取类型标签类型
        getTypeTagType(type) {
            const typeMap = {
                1: 'primary',
                2: 'success',
                3: 'warning',
                4: 'info'
            };
            return typeMap[type] || 'info';
        },
        
        // 获取类型文本
        getTypeText(type) {
            const typeMap = {
                1: '篮球场',
                2: '羽毛球场',
                3: '网球场',
                4: '游泳池'
            };
            return typeMap[type] || '其他';
        },
        
        // 处理搜索
        handleSearch() {
            this.currentPage = 1;
            this.loadFacilities();
        },
        
        // 处理筛选
        handleFilter() {
            this.currentPage = 1;
            this.loadFacilities();
        },
        
        // 处理分页
        handlePageChange(page) {
            this.currentPage = page;
            this.loadFacilities();
        },
        
        // 处理每页条数变化
        handleSizeChange(size) {
            this.pageSize = size;
            this.currentPage = 1;
            this.loadFacilities();
        },
        
        // 打开新增场馆对话框
        handleAdd() {
            this.dialogMode = 'add';
            this.facilityForm = {
                facility_name: '',
                type: '',
                location: '',
                capacity: '',
                area: '',
                price: '',
                description: '',
                status: 1,
                opening_hours: '06:00-22:00',
                advance_booking_days: 7,
                min_booking_duration: 1,
                max_booking_duration: 4,
                sort_order: 0,
                image_url: this.getDefaultImageByType('')
            };
            this.dialogVisible = true;
            this.$nextTick(() => {
                this.$refs.facilityForm.clearValidate();
            });
        },
        
        // 编辑场馆
        editFacility(row) {
            this.dialogMode = 'edit';
            this.selectedFacility = row;
            this.facilityForm = {
                facility_id: row.facility_id,
                facility_name: row.facility_name,
                type: row.type,
                description: row.description,
                price: row.price,
                status: row.status,
                image_url: row.image_url || this.getDefaultImageByType(row.type),
                min_booking_duration: row.min_booking_duration,
                max_booking_duration: row.max_booking_duration,
                sort_order: row.sort_order,
                location: row.location,
                capacity: row.capacity,
                area: row.area,
                opening_hours: row.opening_hours,
                advance_booking_days: row.advance_booking_days
            };
            this.dialogVisible = true;
            if (this.$refs.facilityForm) {
                this.$refs.facilityForm.clearValidate();
            }
        },
        
        // 查看场馆详情
        handleView(row) {
            this.selectedFacility = row;
            this.viewDialogVisible = true;
        },
        
        // 删除场馆
        deleteFacility(row) {
            this.$confirm('确认删除该场馆吗？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                api.facilities.delete(row.facility_id).then(response => {
                    this.$message.success('删除成功');
                    this.loadFacilities();
                }).catch(error => {
                    console.error('删除失败:', error);
                    this.$message.error('删除失败');
                });
            }).catch(() => {});
        },
        
        // 提交表单
        submitForm() {
            this.$refs.facilityForm.validate((valid) => {
                if (valid) {
                    const data = {
                        ...this.facilityForm,
                        price: parseFloat(this.facilityForm.price),
                        image_url: this.facilityForm.image_url || this.getDefaultImageByType(this.facilityForm.type),
                        status: parseInt(this.facilityForm.status),
                        capacity: parseInt(this.facilityForm.capacity),
                        area: parseFloat(this.facilityForm.area),
                        advance_booking_days: parseInt(this.facilityForm.advance_booking_days)
                    };
                    
                    const request = this.facilityForm.facility_id
                        ? api.facilities.update(this.facilityForm.facility_id, data)
                        : api.facilities.create(data);
                    
                    request.then(response => {
                        this.$message.success(this.facilityForm.facility_id ? '更新成功' : '添加成功');
                        this.dialogVisible = false;
                        this.loadFacilities();
                    }).catch(error => {
                        console.error(this.facilityForm.facility_id ? '更新失败:' : '添加失败:', error);
                        this.$message.error(this.facilityForm.facility_id ? '更新失败' : '添加失败');
                    });
                }
            });
        },
        
        // 处理用户下拉菜单命令
        handleUserCommand(command) {
            if (command === 'logout') {
                Auth.logout();
                window.location.href = '/index.html';
            }
        },
        
        // 重置表单
        resetForm() {
            this.facilityForm = {
                facility_name: '',
                type: '',
                location: '',
                capacity: '',
                area: '',
                price: '',
                description: '',
                status: 1,
                opening_hours: '06:00-22:00',
                advance_booking_days: 7,
                min_booking_duration: 1,
                max_booking_duration: 4,
                sort_order: 0,
                image_url: this.getDefaultImageByType('')
            };
            if (this.$refs.facilityForm) {
                this.$refs.facilityForm.resetFields();
            }
        },
        
        // 格式化时间
        formatTime(timestamp) {
            return dayjs(timestamp).format('YYYY-MM-DD HH:mm:ss');
        },
        
        // 页面跳转
        goToPage(page) {
            this.activeMenu = page;
            const pageMap = {
                dashboard: 'dashboard.html',
                facilities: 'facilities.html',
                bookings: 'bookings.html',
                reports: 'reports.html'
            };
            if (pageMap[page] && page !== 'facilities') {
                window.location.href = pageMap[page];
            }
        },
        
        // 加载场馆类型
        loadFacilityTypes() {
            api.facilities.getTypes()
                .then(response => {
                    if (response.success && Array.isArray(response.data)) {
                        this.facilityTypes = response.data;
                        console.log('加载的场馆类型数据:', this.facilityTypes);
                    } else {
                        console.error('获取场馆类型失败:', response);
                        this.facilityTypes = [];
                    }
                })
                .catch(error => {
                    console.error('获取场馆类型失败:', error);
                    this.facilityTypes = [];
                });
        },
        
        // 根据场馆类型获取默认图片
        getDefaultImageByType(type) {
            const imageMap = {
                'basketball': 'https://images.unsplash.com/photo-1546519638-68e109acd27b?w=800&auto=format&fit=crop',
                'football': 'https://images.unsplash.com/photo-1508098682722-e99c643e5e76?w=800&auto=format&fit=crop',
                'tennis': 'https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=800&auto=format&fit=crop',
                'badminton': 'https://images.unsplash.com/photo-1610555356070-d0efb6505f81?w=800&auto=format&fit=crop',
                'swimming': 'https://images.unsplash.com/photo-1560089000-7433a4ebbd64?w=800&auto=format&fit=crop',
                'gym': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800&auto=format&fit=crop',
                'volleyball': 'https://images.unsplash.com/photo-1592659762303-90081d34b277?w=800&auto=format&fit=crop',
                'table_tennis': 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=800&auto=format&fit=crop',
                'default': 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=800&auto=format&fit=crop'
            };
            return imageMap[type] || imageMap.default;
        },

        // 监听场馆类型变化
        handleTypeChange(type) {
            if (!this.facilityForm.image_url || this.facilityForm.image_url === this.getDefaultImageByType('')) {
                this.facilityForm.image_url = this.getDefaultImageByType(type);
            }
        }
    }
}); 