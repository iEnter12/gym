import { api } from '../../../utils/api.js';
import { Auth } from '../../../utils/auth.js';
import dayjs from '../../../utils/dayjs.min.js';

export default {
    data() {
        return {
            userInfo: {
                username: '',
                real_name: '',
                avatar: ''
            },
            statistics: {
                totalBookings: 0,
                activeBookings: 0,
                completedBookings: 0,
                totalReviews: 0
            },
            recentBookings: [],
            loading: false,
            carouselItems: [
                {
                    title: '专业健身器材',
                    description: '配备先进的健身设备，满足您的各种训练需求',
                    image: '../../assets/images/carousel/equipment.jpg'
                },
                {
                    title: '专业教练团队',
                    description: '经验丰富的教练团队，为您提供专业的指导',
                    image: '../../assets/images/carousel/trainer.jpg'
                },
                {
                    title: '舒适环境',
                    description: '宽敞明亮的训练空间，让您享受健身的乐趣',
                    image: '../../assets/images/carousel/environment.jpg'
                }
            ]
        };
    },
    mounted() {
        this.checkAuth();
        this.loadUserInfo();
        this.loadStatistics();
        this.loadRecentBookings();
    },
    methods: {
        checkAuth() {
            if (!Auth.isAuthenticated()) {
                this.$message.error('请先登录');
                this.$router.push('/login');
            }
        },
        async loadUserInfo() {
            try {
                const response = await api.get('/accounts/user-info/');
                this.userInfo = response.data;
            } catch (error) {
                console.error('获取用户信息失败:', error);
            }
        },
        async loadStatistics() {
            try {
                this.loading = true;
                const response = await api.get('/bookings/statistics/');
                this.statistics = response.data;
            } catch (error) {
                this.$message.error('加载统计数据失败');
                console.error('加载统计数据失败:', error);
            } finally {
                this.loading = false;
            }
        },
        async loadRecentBookings() {
            try {
                const response = await api.get('/bookings/recent/');
                this.recentBookings = response.data;
            } catch (error) {
                this.$message.error('加载最近预约失败');
                console.error('加载最近预约失败:', error);
            }
        },
        formatDate(date) {
            return dayjs(date).format('YYYY-MM-DD HH:mm');
        },
        formatStatus(status) {
            const statusMap = {
                pending: '待确认',
                confirmed: '已确认',
                completed: '已完成',
                cancelled: '已取消'
            };
            return statusMap[status] || status;
        },
        goToPage(page) {
            this.$router.push(`/user/${page}`);
        },
        logout() {
            Auth.logout();
            this.$router.push('/login');
        }
    }
}; 