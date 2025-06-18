new Vue({
    el: '#app',
    data() {
        return {
            adminInfo: {
                username: '',
                avatar: ''
            },
            sidebarCollapsed: false,
            activeMenu: 'bookings',
            loading: false,
            searchKeyword: '',
            statusFilter: '',
            dateRange: [],
            currentPage: 1,
            pageSize: 10,
            total: 0,
            bookings: [],
            filteredBookings: [],
            bookingStats: {
                total: 0,
                pending: 0,
                confirmed: 0,
                completed: 0
            },
            viewDialogVisible: false,
            selectedBooking: null,
            facilities: [],
            bookingStatus: [],
            facilityTypes: [],
            statusFilter: '',
            dateFilter: '',
            facilityFilter: '',
            filterForm: {
                status: '',
                dateRange: [],
                facility_id: '',
                keyword: ''
            }
        }
    },
    created() {
        this.checkAuth();
        this.loadAdminInfo();
        this.loadBookings();
        this.loadFacilityTypes();
    },
    methods: {
        // 检查登录状态
        checkAuth() {
            if (!Auth.requireAdmin()) {
                return;
            }
        },
        
        // 加载管理员信息
        loadAdminInfo() {
            const adminInfo = Auth.getUserInfo();
            if (adminInfo) {
                this.adminInfo = adminInfo;
            }
        },
        
        // 加载预约列表
        loadBookings() {
            this.loading = true;
            
            api.bookings.getList()
                .then(response => {
                    console.log('预约列表响应:', response);
                    if (response.success && response.data) {
                        this.bookings = response.data;
                    } else if (response.results) {
                        this.bookings = response.results;
                    } else if (response.data) {
                        this.bookings = response.data.results || response.data;
                    } else {
                        this.bookings = [];
                    }
                    
                    // 应用前端分页和筛选
                    this.filterBookings();
                    
                    this.loading = false;
                })
                .catch(error => {
                    console.error('获取预约列表失败:', error);
                    this.$message.error('获取预约列表失败');
                    this.bookings = [];
                    this.filteredBookings = [];
                    this.total = 0;
                    this.loading = false;
                });
        },
        
        // 加载场馆列表
        loadFacilities() {
            api.facilities.getList()
                .then(response => {
                    if (response.success) {
                        this.facilities = response.data;
                    }
                })
                .catch(error => {
                    console.error('获取场馆列表失败:', error);
                });
        },
        
        // 加载场馆类型
        loadFacilityTypes() {
            api.facilities.getTypes()
                .then(response => {
                    this.facilityTypes = response.results || response.data?.results || response.data || [];
                })
                .catch(error => {
                    console.error('获取场馆类型失败:', error);
                });
        },
        
        // 加载预约状态
        loadBookingStatus() {
            this.bookingStatus = [
                { value: 0, label: '待确定' },
                { value: 1, label: '已确定' },
                { value: 2, label: '已完成' }
            ];
        },
        
        // 更新预约统计
        updateBookingStats() {
            // 根据当前列表数据计算统计信息
            this.bookingStats = {
                total: this.filteredBookings.length,
                pending: this.filteredBookings.filter(b => b.status === 0).length,
                confirmed: this.filteredBookings.filter(b => b.status === 1).length,
                completed: this.filteredBookings.filter(b => b.status === 2).length
            };
        },
        
        // 前端分页和筛选
        filterBookings() {
            let filtered = [...this.bookings];
            
            // 状态筛选
            if (this.statusFilter !== '') {
                filtered = filtered.filter(booking => booking.status === parseInt(this.statusFilter));
            }
            
            // 日期筛选
            if (this.dateRange && this.dateRange.length === 2) {
                const startDate = new Date(this.dateRange[0]);
                const endDate = new Date(this.dateRange[1]);
                filtered = filtered.filter(booking => {
                    const bookingDate = new Date(booking.booking_date);
                    return bookingDate >= startDate && bookingDate <= endDate;
                });
            }
            
            // 场馆筛选
            if (this.facilityFilter) {
                filtered = filtered.filter(booking => booking.facility_id === this.facilityFilter);
            }
            
            // 搜索关键词筛选
            if (this.searchKeyword) {
                const keyword = this.searchKeyword.toLowerCase();
                filtered = filtered.filter(booking => 
                    booking.facility_name.toLowerCase().includes(keyword) ||
                    booking.account_username.toLowerCase().includes(keyword) ||
                    booking.account_real_name?.toLowerCase().includes(keyword)
                );
            }
            
            this.total = filtered.length;
            
            // 分页
            const start = (this.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            this.filteredBookings = filtered.slice(start, end);
            
            this.updateBookingStats();
        },
        
        // 搜索处理
        handleSearch() {
            this.currentPage = 1;
            this.filterBookings();
        },
        
        // 筛选处理
        handleFilter() {
            this.currentPage = 1;
            this.filterBookings();
        },
        
        // 日期筛选处理
        handleDateFilter() {
            this.currentPage = 1;
            this.filterBookings();
        },
        
        // 分页大小改变
        handleSizeChange(size) {
            console.log('改变每页显示数量:', size);
            this.pageSize = parseInt(size);  // 确保是数字
            this.currentPage = 1;  // 重置到第一页
            this.filterBookings();
        },
        
        // 当前页改变
        handlePageChange(page) {
            console.log('切换到页码:', page);
            this.currentPage = parseInt(page);  // 确保是数字
            this.filterBookings();
        },
        
        // 表格选择改变
        handleSelectionChange(selection) {
            // 处理表格行选择变化
            console.log('选择的行:', selection);
        },
        
        // 查看预约
        handleView(row) {
            this.loading = true;
            api.bookings.getDetail(row.booking_id)
                .then(response => {
                    console.log('预约详情响应:', response);
                    if (response.success) {
                        this.selectedBooking = response.data;
                        this.viewDialogVisible = true;
                    } else {
                        this.$message.error(response.message || '获取预约详情失败');
                    }
                })
                .catch(error => {
                    console.error('获取预约详情失败:', error);
                    this.$message.error('获取预约详情失败');
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        
        // 确认预约
        handleConfirm(row) {
            this.$confirm('确定要确认该预约吗？', '提示', {
                type: 'warning'
            }).then(() => {
                api.bookings.confirm(row.booking_id)
                    .then(response => {
                        if (response.success) {
                            this.$message.success('预约已确认');
                            this.loadBookings();
                            this.updateBookingStats();
                        }
                    })
                    .catch(error => {
                        console.error('确认预约失败:', error);
                    });
            }).catch(() => {});
        },
        
        // 完成预约
        handleComplete(row) {
            this.$confirm('确定要完成该预约吗？', '提示', {
                type: 'warning'
            }).then(() => {
                api.bookings.complete(row.booking_id)
                    .then(response => {
                        if (response.success) {
                            this.$message.success('预约已完成');
                            this.loadBookings();
                            this.updateBookingStats();
                        }
                    })
                    .catch(error => {
                        console.error('完成预约失败:', error);
                    });
            }).catch(() => {});
        },
        
        // 取消预约
        handleCancel(booking) {
            this.$confirm('确定要取消该预约吗？取消后预约将被删除。', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                api.bookings.cancel(booking.booking_id)
                    .then(response => {
                        if (response.success) {
                            this.$message.success('预约已取消');
                            this.loadBookings();
                            this.updateBookingStats();
                        }
                    })
                    .catch(error => {
                        console.error('取消预约失败:', error);
                    });
            }).catch(() => {});
        },
        
        // 获取状态文本
        getStatusText(status) {
            const statusMap = {
                0: '待确认',
                1: '已确认',
                2: '已完成',
                3: '已取消'
            };
            return statusMap[status] || '未知状态';
        },
        
        // 获取状态类型
        getStatusType(status) {
            const typeMap = {
                0: 'warning',
                1: 'primary',
                2: 'success',
                3: 'info'
            };
            return typeMap[status] || 'info';
        },
        
        // 格式化日期
        formatDate(date) {
            return dayjs(date).format('YYYY-MM-DD');
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
                bookings: 'bookings.html'
            };
            if (pageMap[page] && page !== 'bookings') {
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
        
        // 格式化日期为API所需的格式 (YYYY-MM-DD)
        formatDateForAPI(date) {
            if (!date) return '';
            const d = new Date(date);
            const year = d.getFullYear();
            const month = String(d.getMonth() + 1).padStart(2, '0');
            const day = String(d.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        },
        
        resetFilter() {
            this.filterForm = {
                status: '',
                dateRange: [],
                facility_id: '',
                keyword: ''
            };
            this.currentPage = 1;
            this.loadBookings();
        }
    }
});
