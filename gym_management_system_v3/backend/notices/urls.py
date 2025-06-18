from django.urls import path
from . import views

urlpatterns = [
    # 公告管理
    path('', views.NoticeListView.as_view(), name='notice_list'),
    path('active/', views.active_notices_view, name='active_notices'),
    path('<int:notice_id>/', views.NoticeDetailView.as_view(), name='notice_detail'),
    path('<int:notice_id>/toggle-status', views.toggle_notice_status_view, name='toggle_notice_status'),
    path('<int:notice_id>/toggle-top', views.toggle_notice_top_view, name='toggle_notice_top'),
]

