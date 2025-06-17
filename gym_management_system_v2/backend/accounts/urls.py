from django.urls import path
from . import views

urlpatterns = [
    # 认证相关
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # 用户信息
    path('user/', views.user_info_view, name='user_info'),
    path('profile/', views.update_profile_view, name='update_profile'),
    path('password/', views.change_password_view, name='change_password'),
    
    # 用户管理（管理员）
    path('', views.UserListView.as_view(), name='user_list'),
    path('<int:user_id>/status/', views.update_user_status_view, name='update_user_status'),
    path('<int:user_id>/reset-password/', views.reset_user_password_view, name='reset_user_password'),
]

