from django.urls import path
from . import views

urlpatterns = [
    # 预约管理
    path('', views.BookingListView.as_view(), name='booking_list'),
    path('create/', views.create_booking_view, name='create_booking'),
    path('user/', views.BookingListView.as_view(), name='user_booking_list'),
    path('<int:booking_id>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('<int:booking_id>/cancel/', views.cancel_booking_view, name='cancel_booking'),
    path('<int:booking_id>/confirm/', views.confirm_booking_view, name='confirm_booking'),
    path('<int:booking_id>/complete/', views.complete_booking_view, name='complete_booking'),
    
    # 统计数据
    path('dashboard/', views.dashboard_statistics_view, name='dashboard_statistics'),
    path('user/stats/', views.user_stats_view, name='user_stats'),
]

