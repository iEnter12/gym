import { api } from '../../../utils/api.js';
import { Auth } from '../../../utils/auth.js';
import dayjs from '../../../utils/dayjs.min.js';

export default {
    data() {
        return {
            facilities: [],
            loading: false,
            dialogVisible: false,
            currentFacility: null,
            bookingForm: {
                facility: '',
                date: '',
                time_slot: '',
                duration: 1
            },
            rules: {
                date: [
                    { required: true, message: '请选择预约日期', trigger: 'change' }
                ],
                time_slot: [
                    { required: true, message: '请选择时间段', trigger: 'change' }
                ],
                duration: [
                    { required: true, message: '请选择时长', trigger: 'change' }
                ]
            },
            timeSlots: [
                { value: '08:00', label: '08:00-09:00' },
                { value: '09:00', label: '09:00-10:00' },
                { value: '10:00', label: '10:00-11:00' },
                { value: '11:00', label: '11:00-12:00' },
                { value: '14:00', label: '14:00-15:00' },
                { value: '15:00', label: '15:00-16:00' },
                { value: '16:00', label: '16:00-17:00' },
                { value: '17:00', label: '17:00-18:00' },
                { value: '18:00', label: '18:00-19:00' },
                { value: '19:00', label: '19:00-20:00' }
            ],
            durations: [
                { value: 1, label: '1小时' },
                { value: 2, label: '2小时' },
                { value: 3, label: '3小时' }
            ]
        };
    },
    mounted() {
        this.checkAuth();
        this.loadFacilities();
    },
    methods: {
        checkAuth() {
            if (!Auth.isAuthenticated()) {
                this.$message.error('请先登录');
                this.$router.push('/login');
            }
        },
        async loadFacilities() {
            try {
                this.loading = true;
                const response = await api.get('/facilities/');
                this.facilities = response.data;
            } catch (error) {
                this.$message.error('加载场馆信息失败');
                console.error('加载场馆信息失败:', error);
            } finally {
                this.loading = false;
            }
        },
        showBookingDialog(facility) {
            this.currentFacility = facility;
            this.bookingForm.facility = facility.id;
            this.dialogVisible = true;
        },
        async submitBooking() {
            try {
                const response = await api.post('/bookings/', this.bookingForm);
                this.$message.success('预约成功');
                this.dialogVisible = false;
                this.$router.push('/user/profile');
            } catch (error) {
                this.$message.error('预约失败');
                console.error('预约失败:', error);
            }
        },
        formatPrice(price) {
            return `¥${price}/小时`;
        }
    }
}; 